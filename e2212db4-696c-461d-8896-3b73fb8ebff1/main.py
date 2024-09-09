from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize the strategy with the ticker(s) of interest
        self.tickers = ["NVDA"]

    @property
    def interval(self):
        # Define the data interval to be used for SMA calculation
        return "1day"

    @property
    def assets(self):
        # Define the assets that this strategy will trade
        return self.tickers

    def run(self, data):
        # Implement the trading logic here
        nvda_prices = data["ohlcv"]["NVDA"]  # Assuming data structure consistency
        current_price = nvda_prices["close"][-1]  # Get the latest closing price
        
        # Calculate the 20-day simple moving average for NVDA
        sma_20 = SMA("NVDA", nvda_prices, length=20)[-1]
        
        # Decide the action based on the current price vs SMA-20
        nvda_allocation = 0.0  # Default to no allocation
        if current_price > sma_20:
            log("NVDA price is above 20-day SMA, buying signal.")
            nvda_allocation = 1.0  # Allocate 100% to NVDA if price > SMA-20
        else:
            log("NVDA price is below 20-day SMA, selling signal or avoid buying.")
            # nvda_allocation remains 0.0 implying sell or not to buy
        
        return TargetAllocation({"NVDA": nvda_allocation})