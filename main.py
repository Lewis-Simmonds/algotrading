# Main execution loop

from scripts.data_handler import DataHandler
from scripts.strategies import SMAStrategy
from scripts.portfolio import Portfolio
from scripts.execution_handler import SimulatedExecutionHandler
from scripts.results import show_results
import pandas as pd
import matplotlib.pyplot as plt
import queue


def run_backtest(csv_file):
    # Setup
    events = queue.Queue()
    symbol = "BTCUSD"

    # Initialise components
    data = DataHandler(symbol, events, csv_file)
    strategy = SMAStrategy(data, events)
    portfolio = Portfolio(data, events)
    broker = SimulatedExecutionHandler(events, data)

    print("Starting backtest...")

    # Event loop
    while data.continue_backtest:
        # Feed next bar of market data
        data.update_bars()
        
        # Process all events in the queue
        while True:
            try:
                event = events.get(False) # Non-blocking get
            except queue.Empty:
                break

            if event.type == 'MARKET':
                strategy.calculate_signals(event)
                portfolio.update_market_value() # Mark to market every bar
            
            elif event.type == 'SIGNAL':
                portfolio.update_signal(event)
            
            elif event.type == 'ORDER':
                broker.execute_order(event)

            elif event.type == 'FILL':
                portfolio.update_fill(event)
    
    # Analysis logic with safety check
    if not portfolio.all_holdings:
        print("Error: No data was logged. Check if your CSV is being read correctly.")
        return None

    stats = pd.DataFrame(portfolio.all_holdings)
    stats.set_index('timestamp', inplace=True)

    print("\nBacktest Finished.")
    print(f"Final Total Portfolio Value: ${stats['total'][-1]:.2f}")
    print(f"Total Return: {((stats['total'][-1] / stats['total'][0]) - 1) * 100:.2f}%")

    return stats


if __name__ == "__main__":
    # Run backtest
    results = run_backtest('./backtesting_data/dummy_data2.csv')

    show_results(results)




