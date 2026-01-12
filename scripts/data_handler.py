# Contains logic for handling and processing market data into strategy-ready format
# CURRENTLY BACKTESTING ONLY    

from .events import MarketEvent
import pandas as pd

class DataHandler:
    def __init__(self, symbol, event_queue, csv_path):
        self.symbol = symbol
        self.event_queue = event_queue
        self.csv_path = csv_path
        self.data = pd.DataFrame()
        self.latest_data = [] # List of bars
        self.continue_backtest = True

        self._load_data()
        self._data_generator = self.data.iterrows()

    def _load_data(self):
        """Load CSV and standarize columns."""
        try:
            self.data = pd.read_csv(self.csv_path)
            print(f"--- DEBUG: Loaded {len(self.data)} rows from {self.csv_path} ---")
            if self.data.empty:
                print("--- DEBUG: CSV is empty! ---")
            
            # Standardization
            self.data.columns = self.data.columns.str.strip().str.lower()
            print(f"--- DEBUG: Columns found: {list(self.data.columns)} ---")
            
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'], unit='s')
            self.data.set_index('timestamp', inplace=True)
            self.data.sort_index(inplace=True)
        except Exception as e:
            print(f"--- DEBUG: Failed to load CSV: {e} ---")

    def get_latest_bars(self, n=1):
        """Return the last n bars from the latest_data list."""
        return self.latest_data[-n:]
    
    def get_latest_bar_value(self, val_type):
        """Helper to get specific value from the latest bar."""
        return getattr(self.latest_data[-1], val_type)
    
    def update_bars(self):
        try:
            # Get the next row from the dataframe
            index, row = next(self._data_generator)
            
            # Create a simple Bar object
            class Bar: pass
            bar = Bar()
            bar.timestamp = index
            for col in row.index:
                setattr(bar, col, row[col])
            
            self.latest_data.append(bar)
            
            # THIS IS CRITICAL:
            self.event_queue.put(MarketEvent())
            
        except StopIteration:
            self.continue_backtest = False
