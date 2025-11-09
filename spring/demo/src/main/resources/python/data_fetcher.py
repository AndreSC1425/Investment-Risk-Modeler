import yfinance as yf
import pandas as pd
import numpy as np
import datetime

START_DATE = (datetime.date.today() - datetime.timedelta(days=5 * 365)).strftime('%Y-%m-%d')

def fetch_and_process_data(tickers):
    try:
        print(f"Fetching data for {tickers} starting from {START_DATE}...")
        data = yf.download(tickers, start=START_DATE)['Close']
        
        if data.empty:
            raise ValueError("No data returned from yfinance. Check ticker symbols.")

        log_returns = np.log(data / data.shift(1))

        log_returns = log_returns.dropna()
        
        print("Data processing complete.")
        return log_returns

    except Exception as e:
        print(f"An error occurred during data fetching: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    TEST_TICKERS = ['AAPL', 'MSFT', 'JPM', 'SPY'] 
    returns_df = fetch_and_process_data(TEST_TICKERS)
    
    if not returns_df.empty:
        print("\n--- Head of Log Returns Data ---")
        print(returns_df.head())
        print(f"\nDataFrame shape: {returns_df.shape}")