import unittest
from unittest.mock import mock_open, patch
from datetime import datetime
from utils.convert import try_parse_int, try_parse_float, timestamp_to_datetime
from utils.csv import read_stock_data

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.valid_csv_data = \
            """symbol,type,last_dividend,fixed_dividend,par_value
            TEA,Common,0.00,,1.00
            POP,Common,0.08,,1.00
            ALE,Common,0.23,,6.0
            GIN,Preferred,0.08,0.02,1.00
            JOE,Common,0.13,,2.50"""

        self.invalid_csv_stock_data = \
            """symbol,type,last_dividend,fixed_dividend,par_value
            TEA,Common,0.00,,1.00
            POP,Common,wrong,wrong,1.00
            ALE,wrong,0.23,,wrong
            GIN,Preferred,0.08,0.02,1.00
            JOE,Common,0.13,,2.50"""

        self.invalid_csv_missing_headers = \
            """symbol,type,last_dividend
            TEA,Common,0.00
            POP,Common,0.08
            ALE,Common,0.23"""

        self.invalid_csv_additional_columns = \
            """symbol,type,last_dividend,fixed_dividend,par_value
            TEA,Common,0.00,,1.00
            POP,Common,0.08,,1.00,extra_data
            ALE,Common,0.23,,6.0,more_data"""

    def test_try_parse_int_valid(self):
        result = try_parse_int("123")
        self.assertEqual(result, 123)

    def test_try_parse_int_invalid(self):
        result = try_parse_int("abc")
        self.assertIsNone(result)

    def test_try_parse_float_valid(self):
        result = try_parse_float("12.34")
        self.assertAlmostEqual(result, 12.34)

    def test_try_parse_float_invalid(self):
        result = try_parse_float("xyz")
        self.assertIsNone(result)

    def test_timestamp_to_datetime_valid(self):
        result = timestamp_to_datetime(111111) 
        self.assertIsInstance(result, datetime)

    def test_timestamp_to_datetime_invalid(self):
        result = timestamp_to_datetime("invalid_timestamp")
        self.assertIsNone(result)

#================================================================
    def test_read_stock_data_invalid_patj(self):
        result = read_stock_data('invalid_path.csv', skip_on_error=True)
        self.assertIsInstance(result, str)

    def test_read_stock_data_valid_csv(self):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data=self.valid_csv_data):
                result = read_stock_data('valid_stock_data.csv', skip_on_error=True)
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 5)

    def test_read_stock_data_invalid_csv_missing_headers(self):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data=self.invalid_csv_missing_headers):
                result = read_stock_data('invalid_stock_data.csv', skip_on_error=True)
                self.assertIsInstance(result, str)

    def test_read_stock_data_invalid_csv_additional_columns(self):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data=self.invalid_csv_additional_columns):
                result = read_stock_data('invalid_stock_data.csv', skip_on_error=True)
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 1)

    def test_read_stock_data_invalid_csv_stop_on_error(self):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data=self.invalid_csv_additional_columns):
                result = read_stock_data('invalid_stock_data.csv', skip_on_error=False)
                self.assertIsInstance(result, str)
    
    def test_read_stock_data_invalid_csv_stock_data(self):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data=self.invalid_csv_stock_data):
                result = read_stock_data('invalid_stock_data.csv', skip_on_error=True)
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 3)

    def test_read_stock_data_invalid_csv_stock_data_stop_on_error(self):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', new_callable=mock_open, read_data=self.invalid_csv_stock_data):
                result = read_stock_data('invalid_stock_data.csv', skip_on_error=False)
                self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()