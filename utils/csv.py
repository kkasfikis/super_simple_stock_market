import csv
from pathlib import Path
from models.stock import Stock,StockType
from utils.convert import try_parse_float

expected_csv_headers = ["symbol", "type", "last_dividend", "fixed_dividend", "par_value"]

def check_file_exists(file_path : str) -> bool:
    """
    Check if a file exists at the specified path.
    Args:
    - file_path (str): The path to the file.
    Returns:
    - bool: True if the file exists, False otherwise.
    """
    return Path(file_path).is_file()

def load_csv(file_path : str) -> list[dict]|str:
    """
    Load data from a CSV file.
    Args:
    - file_path (str): The path to the CSV file.
    Returns:
    - list[dict] | str: A list of dictionaries representing rows if successful, an error message otherwise.
    """
    try:
        with open(file_path,newline='') as csv_file:
            reader = csv.DictReader(csv_file, restval=None, restkey='additional_columns')
            headers = reader.fieldnames
            if headers != expected_csv_headers:
                return "Invalid headers in csv file"
            return [x for x in reader]
    except Exception as e:
        return str(e)
        

def init_stock(row : dict, index : int) -> Stock|str:
    """
    Initialize a Stock object from a dictionary.
    Args:
    - row (dict): The dictionary representing a row from the CSV file.
    - index (int): The index of the row.
    Returns:
    - Stock | str: The initialized Stock object if successful, an error message otherwise.
    """
    try:
        symbol = row['symbol']
        stock_type = row['type'].lower().capitalize()
        last_dividend = try_parse_float(row['last_dividend'])
        fixed_dividend = try_parse_float(row['fixed_dividend'])
        par_value = try_parse_float(row['par_value'])
        additional_columns = row['additional_columns'] if 'additional_columns' in row else None
        if stock_type not in ['Common','Preferred']:
            raise Exception(f'Invalid type in row {index}')
        else:
            stock_type = StockType.Common if stock_type == 'Common' else StockType.Preferred
        
        if additional_columns is not None and len(additional_columns) > 0:
            raise Exception(f'Additional columns detected in row {index}')
        
        return Stock(
            symbol,
            last_dividend,
            fixed_dividend if fixed_dividend is not None else 0,
            par_value,
            type=stock_type
        )
    except Exception as e:
        return str(e)
    
def read_stock_data(file_path:str, skip_on_error:bool = True) -> list[Stock]|str:
    """
    Read stock data from a CSV file.
    Args:
    - file_path (str): The path to the CSV file.
    - skip_on_error (bool): If True, skip rows with errors. If False, stop processing on the first error.
    Returns:
    - list[Stock] | str: A list of Stock objects if successful, an error message otherwise.
    """
    if not check_file_exists(file_path):
        return "[Error] File does not exist"

    stock_data : list[Stock] = []
    rows : list[dict] = load_csv(file_path)
    
    if type(rows) == str:
        return f"[Error] Invalid csv file. {rows}"
    
    for index,row in enumerate(rows):
        stock = init_stock(row,index)
        if type(stock) == str:
            if skip_on_error:
                print(f"[Warning] {stock}. Skipped")
                continue
            else:
                return f"[Error] {stock}"
        else:
            stock_data.append(stock)
        
    return stock_data