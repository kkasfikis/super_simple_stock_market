from datetime import datetime

def try_parse_int(value:str) -> int|None:
    """
    Try to parse a string to an integer.
    Args:
    - value (str): The string to be parsed.
    Returns:
    - int | None: The parsed integer if successful, None otherwise.
    """
    try:
        return int(value)
    except ValueError:
        return None
    
def try_parse_float(value:str) -> float|None:
    """
    Try to parse a string to an integer.
    Args:
    - value (str): The string to be parsed.
    Returns:
    - int | None: The parsed integer if successful, None otherwise.
    """
    try:
        return float(value)
    except ValueError:
        return None

def timestamp_to_datetime(value:int) -> datetime|None:
    """
    Convert a timestamp to a datetime object.
    Args:
    - value (int): The timestamp to be converted.
    Returns:
    - datetime | None: The converted datetime object if successful, None otherwise.
    """
    try:
        return datetime.fromtimestamp(float(value))
    except (ValueError, TypeError):
        return None