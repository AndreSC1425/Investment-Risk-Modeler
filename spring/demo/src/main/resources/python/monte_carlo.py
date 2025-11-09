import numpy as np
import pandas as pd
import json
from scipy.stats import norm
from data_fetcher import fetch_and_process_data

NUM_SIMULATIONS = 5000
TRADING_DAYS_IN_YEAR = 252
NUM_DAYS_TO_FORECAST = TRADING_DAYS_IN_YEAR * 5

def run_monte_carlo_simulation(returns_df, weights):
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty. Cannot run simulation.")
        
    cov_matrix = returns_df.cov()
    mean_returns = returns_df.mean()
    
    tickers = list(returns_df.columns)
    weight_array = np.array([weights[t] for t in tickers])
    
    port_mean = np.sum(mean_returns * weight_array) * TRADING_DAYS_IN_YEAR
    port_stdev = np.sqrt(np.dot(weight_array.T, np.dot(cov_matrix, weight_array))) * np.sqrt(TRADING_DAYS_IN_YEAR)
    
    drift = port_mean / TRADING_DAYS_IN_YEAR - (port_stdev**2 / 2) / TRADING_DAYS_IN_YEAR
    
    L = np.linalg.cholesky(cov_matrix)
    
    final_values = []
    
    for _ in range(NUM_SIMULATIONS):
        random_shock = np.dot(L, norm.ppf(np.random.rand(len(tickers), NUM_DAYS_TO_FORECAST))).T
        
        daily_returns = np.exp(drift + random_shock * (port_stdev / np.sqrt(TRADING_DAYS_IN_YEAR)))
        
        portfolio_return_path = np.zeros(NUM_DAYS_TO_FORECAST)
        
        current_portfolio_value = 1.0 
        
        for i in range(NUM_DAYS_TO_FORECAST):
            daily_port_return = np.sum(daily_returns[i] * weight_array)
            current_portfolio_value *= daily_port_return
            portfolio_return_path[i] = current_portfolio_value
            
        final_values.append(current_portfolio_value)
        
    VaR_95 = np.percentile(final_values, 5)
    
    cagr = (np.mean(final_values)**(1/5)) - 1
    
    return {
        'final_distribution': final_values,
        'VaR_95': float(VaR_95),
        'CAGR': float(cagr)
    }

if __name__ == '__main__':
    TEST_PORTFOLIO = {'AAPL': 0.40, 'MSFT': 0.30, 'JPM': 0.20, 'SPY': 0.10}
    
    try:
        returns_df = fetch_and_process_data(list(TEST_PORTFOLIO.keys()))
        
        results = run_monte_carlo_simulation(returns_df, TEST_PORTFOLIO)

        print("\n--- Simulation Results (JSON Output) ---")
        print(json.dumps(results, indent=4))
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"A general error occurred: {e}")
