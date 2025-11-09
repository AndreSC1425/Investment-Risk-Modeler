import sys
import json
import io
from contextlib import redirect_stdout
from data_fetcher import fetch_and_process_data
from monte_carlo import run_monte_carlo_simulation 

if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise ValueError("No JSON input provided.")
            
        request_json = sys.argv[1]
        request_data = json.loads(request_json)
        
        tickers = request_data['tickers']
        weights = {k: v for k, v in request_data['weights'].items()}

        f = io.StringIO()
        with redirect_stdout(f):
            returns_df = fetch_and_process_data(tickers)
        
        results = run_monte_carlo_simulation(returns_df, weights)
        
        print(json.dumps(results))
        
    except Exception as e:
        sys.stderr.write(f"Executor Error: {e}\n")
        sys.exit(1)