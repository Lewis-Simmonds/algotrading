# Logic of all created strategies, add strategy documentation to README.md

from .events import SignalEvent
import pandas as pd

class SMAStrategy:
    """Simple Moving Average Crossover Strategy"""
    def __init__(self, data_handler, event_queue, short_window=50, long_window=200):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.symbol = data_handler.symbol
        self.short_window = short_window
        self.long_window = long_window
        self.bought = False

    def calculate_signals(self, event):
        """Calculate SMA crossover signals and generate SignalEvent."""
        if event.type == 'MARKET':
            bars = self.data_handler.get_latest_bars(n=self.long_window)

            if len(bars) < self.long_window:
                return
        
        # Extract closing prices
        closes = pd.Series([bar.close for bar in bars])

        # Calculate SMAs
        short_sma = closes[-self.short_window:].mean()
        long_sma = closes.mean()  # Use all bars for long SMA

        # Crossover timestamp
        timestamp = bars[-1].timestamp

        # Buy signal
        if short_sma > long_sma and not self.bought:
            print(f"Signal: LONG at {timestamp}, short_sma={short_sma:.2f}, long_sma={long_sma:.2f}")
            signal = SignalEvent(self.symbol, timestamp, 'LONG')
            self.event_queue.put(signal)
            self.bought = True
        
        # Sell signal
        elif short_sma < long_sma and self.bought:
            print(f"Signal: SHORT at {timestamp}, short_sma={short_sma:.2f}, long_sma={long_sma:.2f}")
            signal = SignalEvent(self.symbol, timestamp, 'SHORT')
            self.event_queue.put(signal)
            self.bought = False