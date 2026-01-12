# Contains all logic related to event handling in the application

class Event:
    pass

class MarketEvent(Event):
    """Triggered when new market data is received from the data feed."""
    def __init__(self):
        self.type = 'MARKET'

class SignalEvent(Event):
    """Triggered by Strategy when a trading signal is produced."""
    def __init__(self, symbol, timestamp, signal_type, strength=None):
        self.type = 'SIGNAL'
        self.timestamp = timestamp
        self.symbol = symbol
        self.signal_type = signal_type  # 'BUY' or 'SELL'
        self.strength = strength  # Confidence level of the signal

class OrderEvent(Event):
    """Triggered by Portfolio when an order needs to be placed."""
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type  # 'MARKET' or 'LIMIT'
        self.quantity = quantity
        self.direction = direction  # 'BUY' or 'SELL'

class FillEvent(Event):
    """Triggered by ExecutionHandler when an order is filled in the market."""
    def __init__(self, symbol, timestamp, exchange, quantity, direction, fill_cost, commission=0.0):
        self.type = 'FILL'
        self.timestamp = timestamp
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction  # 'BUY' or 'SELL'
        self.fill_cost = fill_cost
        self.commission = commission