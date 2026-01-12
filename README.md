# Algotrading suite with built in backtesting capabilities and datastreaming

## Main.py contains logic for running event loop. Other dependency scripts saved in 'scripts' folder

### General process loop explained below

1. Initialise `events` as Python queue
2. Create `DataHandler` to process data stream, passing in `symbol`, `events`, and `csv_file` *(to be updated for live data)*
3. Create `Strategy` with chosen strategy defined in **strategy.py**
4. Create `Portfolio` with defined portfolio size etc
5. Create `SimulatedExecutionHandler` to process events such as market data in and order/fill events
6. Start while loop until to run until backtest is finished, fetch next data bar and trigger `MarketEvent` at start of each loop
7. Check if event in queue, if yes then depending on event type take following actions
   * `MarketEvent` - calculate signals from strategy and update market value of `Portfolio`
   * `SignalEvent` - create `OrderEvent` based on direction and sizing from `SignalEvent`
   * `OrderEvent` - execute `OrderEvent` by creating `FillEvent`
   * `FillEvent` - update `Portfolio` with new position and print position taken to log
8. Once while loop finished (no more data), create `DataFrame` with all holdings over backtest period
9. Print `Portfolio` value and total return and plot graph of `Portfolio` value over time

