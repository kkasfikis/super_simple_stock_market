from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from models.stock import Stock

class TradeType(Enum):
    Buy = 1
    Sell = 2

@dataclass
class Trade():
    """
    Represents a trade with its attributes and methods.
    Attributes:
    - stock (Stock): The stock involved in the trade.
    - quantity (int): The quantity of shares traded.
    - type (TradeType): The type of the trade (Buy or Sell).
    - price (float): The price per share.
    - date (datetime): The date and time of the trade.
    """
    stock: Stock
    quantity: int
    type: TradeType
    price: float
    date: datetime = field(default_factory=datetime.now)

    @staticmethod
    def print_trade_list(trades : list['Trade']) -> None:
        """
        Print information about all trades.
        """
        if not len(trades):
            print('No trade data available') 
        else:
            for index,trade in enumerate(trades):
                print(f"{index + 1}.{repr(trade)}")

    def __post_init__(self):
        """
        Validate trade attributes after initialization.
        Raises:
        - ValueError: If any attribute is invalid.
        """
        if self.stock is None:
            raise ValueError("Invalid Trade stock")
        if self.quantity < 1:
            raise ValueError("Invalid Trade quantity")
        if self.price <= 0:
            raise ValueError("Invalid Trade price")
        if self.date > datetime.now():
            raise ValueError("Invalid Trade date")
    
    def __repr__(self):
        """
        Return a string representation of the trade.
        Returns:
        - str: A string representation of the trade.
        """
        return f"""
        Symbol:{self.stock.symbol} 
        Quantity:{self.quantity} 
        Type:{'Buy' if self.type == TradeType.Buy else 'Sell'} 
        Date:{self.date.strftime('%Y/%m/%d %H:%M:%S')}
        """