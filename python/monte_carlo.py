import numpy as np
import pandas as pd
import json
import sys
from scipy.stats import norm
from data_fetcher import fetch_and_process_data

NUM_SIMULATIONS = 5000
TRADING_DAYS_IN_YEAR = 252
NUM_DAYS_TO_FORECAST = TRADING_DAYS_IN_YEAR * 5

def run_monte_carlo_simulation(returns_df, weights):
    if returns_df.empty:
        raise ValueError("Returns DataFrame is empty. Cannot run simulation.")
        
    # Seed the random number generator to ensure different results on each run
    np.random.seed(None)
        
    cov_matrix = returns_df.cov()
    mean_returns = returns_df.mean()
    
    # Filter weights to only include tickers that were successfully fetched
    valid_tickers = [t for t in returns_df.columns if t in weights]
    filtered_weights = {t: weights[t] for t in valid_tickers}

    # Re-align the returns data and covariance matrix to only include valid tickers
    returns_df = returns_df[valid_tickers]
    cov_matrix = returns_df.cov()
    mean_returns = returns_df.mean()
    
    weight_array = np.array([filtered_weights[t] for t in valid_tickers])
    
    port_mean = np.sum(mean_returns * weight_array) * TRADING_DAYS_IN_YEAR
    port_stdev = np.sqrt(np.dot(weight_array.T, np.dot(cov_matrix, weight_array))) * np.sqrt(TRADING_DAYS_IN_YEAR)
    # Calculate the drift and random component for the entire portfolio
    drift = port_mean - (0.5 * port_stdev**2)
    daily_drift = drift / TRADING_DAYS_IN_YEAR
    daily_stdev = port_stdev / np.sqrt(TRADING_DAYS_IN_YEAR)
    
    final_values = []
    
    for _ in range(NUM_SIMULATIONS):
        # Generate random returns for the portfolio for the entire forecast period
        random_returns = np.random.normal(loc=daily_drift, scale=daily_stdev, size=NUM_DAYS_TO_FORECAST)
        # Calculate the cumulative return path
        path = np.exp(np.cumsum(random_returns))
        current_portfolio_value = path[-1]
        final_values.append(current_portfolio_value)
        
    VaR_95 = np.percentile(final_values, 5)
    
    # Calculate CAGR for each simulation path and then average them
    # This is a more conservative approach than averaging final values first
    individual_cagrs = [(value**(1/5)) - 1 for value in final_values]
    average_cagr = np.mean(individual_cagrs)
    
    return {
        'final_distribution': final_values,
        'VaR_95': float(VaR_95),
        'CAGR': float(average_cagr)
    }

if __name__ == '__main__':
    try:
        # Read the JSON input from standard input
        input_json_string = sys.stdin.read()
        request_data = json.loads(input_json_string)
        portfolio_tickers = list(request_data.get('weights', {}).keys())
        portfolio_weights = request_data.get('weights', {})
    except (json.JSONDecodeError) as e:
        print(f"Error parsing stdin JSON: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        returns_df = fetch_and_process_data(portfolio_tickers)
        
        results = run_monte_carlo_simulation(returns_df, portfolio_weights)

        print(json.dumps(results))
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"A general error occurred: {e}", file=sys.stderr)
        sys.exit(1)