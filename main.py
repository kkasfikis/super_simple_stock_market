import argparse
from utils.csv import read_stock_data
from models.stock import Stock
from models.trade import Trade,TradeType
from utils.convert import try_parse_int,try_parse_float,timestamp_to_datetime
from datetime import datetime

stock_data : list[Stock] = []
trade_data : list[Trade] = []

def find_stock_by_ticker(ticker:str) -> Stock|None:
    """
    Find a stock by its ticker symbol.
    Args:
    - ticker (str): The ticker symbol to search for.
    Returns:
    - Stock | None: The found stock if exists, None otherwise.
    """
    return next((x for x in stock_data if x.symbol.lower() == ticker.lower()),None)    

def handle_stock_menu(stock:Stock):
    """
    Handle the stock submenu.
    Args:
    - stock (Stock): The selected stock.
    """

    print("""
    1. Calculate dividend yield of stock
    2. Calculate P/E Ratio of stock
    3. Record a Trade
    4. Calculate Volume Weighted Stock Price
    Input any other key to exit submenu
    """)
    
    choice = input("Select one of the above options: ")
    
    if choice not in ["1","2","3","4"]:
        print("Exiting Submenu..")
        return False

    if choice == "1" or choice == "2":       
        while (price:=try_parse_float(input("Price: "))) is None:
            print(f"Invalid price! Please try again")

        if choice == "1":
            print(f"Calculated dividend yield : { round(stock.calculate_dividend_yield(price),4)}")
        else:
            print(f"Calculated P/E ratio : { round(stock.calculate_pe_ratio(price), 4)}")
    
    elif choice == "3":
        trade = None
        while trade is None:
            while (quantity:=try_parse_int(input("Quantity: "))) is None:
                print(f"Invalid quantity! Please try again")
            while (trade_type:=input('Trade Type (Buy/Sell): ').lower()) not in ['buy','sell']:
                print(f"Invalid Trade Type! Please try again")
            trade_type = TradeType.Buy if trade_type.lower() == 'buy' else TradeType.Sell   
            while (price:=try_parse_float(input("Price: "))) is None:
                print(f"Invalid price! Please try again")
            date = None
            while type(date) != datetime :
                date = input("Date (Leave empty for current date): ")
                if date is not None and not len(date):
                    date = datetime.now()
                else:
                    date=timestamp_to_datetime(date)
                    if date is None:
                        print(f"Invalid date! Please try again")
            try:
                trade = Trade(stock,quantity,trade_type,price,date)
            except Exception as e:
                print(f'Could not create Trade! {str(e)}')
        trade_data.append(trade)        
    
    elif choice == "4":
        print(f'Volume Weighted Stock Price: {round(stock.calculate_volume_weighted_stock_price(trade_data),4)}')

    return True

def handle_menu():
    """
    Handle the main menu.
    """
    print("""
    1. Print all Stocks
    2. Stock Actions
    3. Print all Trades
    4. Calculate GBCE All Share Index
    Input any other key to exit application
    """)
    choice = input("Select one of the above options: ")

    if choice not in ["1","2","3","4"]:
        print("Exiting. Bye Bye")
        return False
    
    if choice == "1":
        Stock.print_stock_list(stock_data)
    
    elif choice == "2":
        while (stock:=find_stock_by_ticker(input("Ticker: "))) is None:
            print(f"Invalid ticker! Please try again")
        while handle_stock_menu(stock):
            pass
    
    elif choice == "3":
        Trade.print_trade_list(trade_data)
    
    elif choice == "4":
        if not len(stock_data):
            print('No stock data available')
        else:
            prices : list[float] = []
            for stock in stock_data:
                while (price:=try_parse_float(input(f"Price for {stock.symbol}: "))) is None or price <= 0:
                    print(f"Invalid price! Please try again")
                prices.append(price)
            print(f'GBCE Stock Index: {round(Stock.calculate_gbce_index(prices),4)}')
    
    return True

def main(file_path:str, skip_csv_errors : bool) -> None:
    """
    The main function to run the application.
    Args:
    - file_path (str): Path to the Stock Data CSV file.
    - skip_csv_errors (bool): Skip row errors on imported CSV.
    """
    global stock_data
    stock_data = read_stock_data(file_path, skip_csv_errors)
    if type(stock_data) == str:
        print(stock_data)
        return
    while handle_menu():
        pass

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Argument Parser Example")
    parser.add_argument('stock_csv_path', type=str, help='Path to the Stock Data CSV file')
    parser.add_argument('--skip_csv_errors', action='store_true', help='Skip row errors on imported CSV')
    args = parser.parse_args()
    return args         

if __name__ == "__main__":
    args = parse_arguments()
    main(args.stock_csv_path, args.skip_csv_errors)