from enum import Enum
from dataclasses import dataclass,field
from datetime import datetime,timedelta
import math

class StockType(Enum):
    Common = 1
    Preferred = 2

@dataclass
class Stock():
    """
    Represents a stock with its attributes and methods.
    Attributes:
    - symbol (str): The symbol or identifier of the stock.
    - last_dividend (float): The last dividend value of the stock.
    - fixed_dividend (float | None): The fixed dividend value for preferred stock, None for common stock.
    - par_value (float): The par value of the stock.
    - type (StockType): The type of the stock (Common or Preferred).
    """
    symbol: str
    last_dividend: float
    fixed_dividend: float
    par_value: float
    type: StockType = field(default=StockType.Common)

    def _calculate_common_dividend_yield(self,price:float) -> float:
        """
        Calculate the common dividend yield for the stock.
        Args:
        - price (float): The current price of the stock.
        Returns:
        - float: The calculated common dividend yield.
        """
        return ( self.last_dividend/price ) if price > 0 else 0

    def _calucalte_preferred_dividend_yield(self,price:float) -> float:
        """
        Calculate the preferred dividend yield for the stock.
        Args:
        - price (float): The current price of the stock.
        Returns:
        - float: The calculated preferred dividend yield.
        """
        return ( (self.fixed_dividend * self.par_value) / price ) if price > 0 else 0

    def calculate_dividend_yield(self,price:float) -> float:
        """
        Calculate the dividend yield based on the stock type.
        Args:
        - price (float): The current price of the stock.
        Returns:
        - float: The calculated dividend yield.
        """
        return self._calculate_common_dividend_yield(price) if self.type == StockType.Common else self._calucalte_preferred_dividend_yield(price)

    def calculate_pe_ratio(self,price:float) -> float:
        """
        Calculate the P/E ratio for the stock.
        Args:
        - price (float): The current price of the stock.
        Returns:
        - float: The calculated P/E ratio.
        """
        return price / self.last_dividend if self.last_dividend > 0 else 0

    def calculate_volume_weighted_stock_price(self, trades : list['Trade']) -> float:
        """
        Calculate the volume-weighted stock price.
        Args:
        - trades (list[Trade]): List of trades for a specific stock.
        Returns:
        - float: The calculated volume-weighted stock price.
        """
        stock_trades = [x for x in trades if x.stock is self and x.date > (datetime.now() - timedelta(minutes=15))]
        numerator = sum(trade.price * trade.quantity for trade in stock_trades)
        denominator = sum(trade.quantity for trade in stock_trades)
        return numerator / denominator if denominator != 0 else 0

    @staticmethod
    def calculate_gbce_index(prices:list[float]) -> float:
        """
        Calculate the GBCE All Share Index.
        Args:
        - prices (list[float]): List of prices for different stocks.
        Returns:
        - float: The calculated GBCE All Share Index.
        """
        return math.prod(prices) ** (1 / len(prices)) if prices else 0
    
    def print_stock_list(stocks : list['Stock']) -> None:
        """
        Print information about all stocks.
        """
        if not len(stocks):
            print('No stock data available') 
        else:
            for index,stock in enumerate(stocks):
                print(f"{index + 1}.{repr(stock)}")
    
    def __post_init__(self):
        """
        Validate stock attributes after initialization.
        Raises:
        - ValueError: If any attribute is invalid.
        """
        if self.symbol is None or not len(self.symbol):
            raise ValueError(f'Invalid symbol')

        if self.last_dividend is None or self.last_dividend < 0:
            raise ValueError(f'Invalid dividend value')
                
        if (self.type == StockType.Common and self.fixed_dividend > 0):
            raise ValueError(f'Common Stock with fixed dividend value')

        if (self.type == StockType.Preferred and not self.fixed_dividend):
            raise ValueError(f'Preferred Stock is missing fixed dividend value')

        if (self.type == StockType.Preferred and self.fixed_dividend <= 0) or self.fixed_dividend > 1:
            raise ValueError(f'Invalid fixed dividend value')

        if self.par_value is None or self.par_value < 0:
            raise ValueError(f'Invalid par value')

    def __repr__(self):
        """
        Return a string representation of the stock.
        Returns:
        - str: A string representation of the stock.
        """
        return f"""
            Symbol:{self.symbol} 
            Type:{'Common' if self.type==StockType.Common else 'Preferred'} 
            Dividend:{self.last_dividend} 
            Fixed Dividend:{self.fixed_dividend if self.type==StockType.Preferred else 'NaN'}
            Par Value:{self.par_value}
        """