# Logic to handle execution of orders

from .events import FillEvent

class SimulatedExecutionHandler:
    """Simulates order execution by immediately filling orders at market price."""
    def __init__(self, event_queue, data_handler):
        self.event_queue = event_queue
        self.data_handler = data_handler

    def execute_order(self, event):
        """Executes an OrderEvent by creating a FillEvent."""
        if event.type == 'ORDER':
            # TODO: In a real engine, need to check order types, liquidity, slippage etc
            # Assuming immediate fill at latest market price
            current_bar = self.data_handler.get_latest_bars(n=1)[0]
            price = current_bar.close
            timestamp = current_bar.timestamp

            # Create FillEvent
            # TODO: Calculate commission properly
            fill = FillEvent(event.symbol, timestamp, 'BACKTESTING', event.quantity, event.direction, price, commission=1.0)
            self.event_queue.put(fill)