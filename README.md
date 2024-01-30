# Super Simple Stock Market

This project implements a simple stock market system with functionalities like :
- calculate stock dividend yield
- calculate stock P/E ratio
- record trades
- calculate volume weighted average price for a stock
- calculate the GBCE All Share Index

## Overview

The project consists of modules, each serving a specific purpose:

- **utils**: Contains utility functions for type conversions and CSV file operations.
- **models**: Defines classes representing stocks and trades.
- **main.py**: Implements the main application logic for interacting with stocks and trades.
- **tests**: Contains unit tests for testing the functionalities of the utility functions and model classes.

## File Structure

```
super_simple_stock_market/
│
├── utils/
│   ├── convert.py
│   └── csv.py
│
├── models/
│   ├── stock.py
│   └── trade.py
│
├── main.py
│
└── tests/
    ├── test_models.py
    └── test_utils.py
```


## Modules

### `utils`

- **convert.py**: Contains utility functions for converting data types and timestamps.
- **csv.py**: Provides functions for handling CSV file operations, such as reading stock data.

### `models`

- **stock.py**: Defines the `Stock` class representing stocks, including methods for calculating dividend yield, P/E ratio, volume-weighted stock price, and GBCE index.
- **trade.py**: Defines the `Trade` class representing trades, including methods for validation and string representation.

### `main.py`

Implements the main application logic for interacting with stocks and trades, including menu-driven options for calculating stock metrics, recording trades, and calculating the GBCE index.

### `tests`

Contains unit tests for testing the functionalities of utility functions and model classes.

- **test_models.py**: Unit tests for the `Stock` and `Trade` classes.
- **test_utils.py**: Unit tests for utility functions in the `utils` module, such as conversion functions and CSV file operations.

## Testing

To run the unit tests, execute the following command from the project root directory:

```bash
python -m unittest discover -s tests
```

## Dependencies
The project has no external dependencies beyond the standard library for Python.

## Usage
To use the application, run the main.py script and follow the menu-driven options to interact with stocks and trades.
```bash
python main.py path/to/stock/data/csv --skip_csv_errors
```