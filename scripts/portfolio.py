# Contains portfolio of capital and open positions

from .events import OrderEvent

class Portfolio:
    def __init__(self, data_handler, event_queue, initial_capital=10000.0):
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.symbol = data_handler.symbol
        self.initial_capital = initial_capital

        # Current positions and holdings
        self.current_positions = {self.symbol: 0}
        self.current_holdings = {
            self.symbol: 0.0, 
            'cash': initial_capital, 
            'total': initial_capital
        }

        # Log of holdings over time
        self.all_holdings = []

    def update_market_value(self):
            """Triggered every time a new bar arrives."""
            latest_bars = self.data_handler.get_latest_bars(n=1)
            if not latest_bars:
                return

            bar = latest_bars[0]
            # Calculate current market value of the position
            market_value = self.current_positions[self.symbol] * bar.close
            
            self.current_holdings[self.symbol] = market_value
            self.current_holdings['total'] = self.current_holdings['cash'] + market_value
            
            # Create a snapshot for the equity curve
            # We explicitly add the 'timestamp' key here
            snapshot = {
                'timestamp': bar.timestamp,
                'cash': self.current_holdings['cash'],
                self.symbol: self.current_holdings[self.symbol],
                'total': self.current_holdings['total']
            }
            self.all_holdings.append(snapshot)

    def update_signal(self, event):
        """Acts on a SignalEvent to generate an Order."""
        if event.type == 'SIGNAL':
            direction = 'BUY' if event.signal_type == 'LONG' else 'SELL'
            # TODO: Implement position sizing logic
            quantity = 1 # Fixed quantity for simplicity

            # TODO: Refine this logic to handle netting
            order = OrderEvent(self.symbol, 'MARKET', quantity, direction)
            print(f"Order created: {direction} {quantity} {self.symbol}")
            self.event_queue.put(order)
    
    def update_fill(self, event):
        """Updates Portfolio positions upon FillEvent."""
        if event.type == 'FILL':
            fill_direction = 1 if event.direction == 'BUY' else -1

            # Update positions
            self.current_positions[event.symbol] += (fill_direction * event.quantity)

            # Update cash (cost of trade + commission)
            cost = fill_direction * event.fill_cost * event.quantity
            self.current_holdings['cash'] -= (cost + event.commission)

            print(f"Filled {event.direction}: {event.quantity} of {event.symbol} at {event.fill_cost}. Commission: {event.commission}")

        