import unittest
from datetime import datetime, timedelta
from models.stock import Stock, StockType
from models.trade import Trade, TradeType

class TestModels(unittest.TestCase):

    def setUp(self):
        self.common_stock = Stock("ABC", 5.0, 0, 10.0, StockType.Common)
        self.preferred_stock = Stock("XYZ", 4.0, 0.02, 15.0, StockType.Preferred)
        self.trade_stock = Stock(symbol="ABC", last_dividend=1.0, fixed_dividend=0, par_value=10.0, type=StockType.Common)

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            Stock(None, 5.0, 0, 10.0, StockType.Common)

    def test_negative_dividend(self):
        with self.assertRaises(ValueError):
            Stock("POP", -5.0, 0, 10.0, StockType.Common)

    def test_common_stock_with_fixed_dividend(self):
        with self.assertRaises(ValueError):
            Stock("POP", 4.0, 0.02, 15.0, StockType.Common)

    def test_preferred_stock_missing_fixed_dividend(self):
        with self.assertRaises(ValueError):
            Stock("POP", 4.0, 0, 15.0, StockType.Preferred)

    def test_invalid_fixed_dividend_value(self):
        with self.assertRaises(ValueError):
            Stock("POP", 4.0, 1.5, 15.0, StockType.Preferred)

    def test_negative_par_value(self):
        with self.assertRaises(ValueError):
            Stock("POP", 5.0, 0, -10.0, StockType.Common)

    def test_calculate_dividend_yield_common(self):
        self.assertAlmostEqual(self.common_stock.calculate_dividend_yield(20.0), 0.25)

    def test_calculate_dividend_yield_preferred(self):
        self.assertAlmostEqual(self.preferred_stock.calculate_dividend_yield(20.0), 0.015)

    def test_calculate_dividend_yield_zero_price(self):
        self.assertEqual(self.common_stock.calculate_dividend_yield(0), 0)
        self.assertEqual(self.preferred_stock.calculate_dividend_yield(0), 0)

    def test_calculate_pe_ratio(self):
        self.assertAlmostEqual(self.common_stock.calculate_pe_ratio(20.0), 4.0)

    def test_calculate_pe_ratio_zero_dividend(self):
        self.assertEqual(self.common_stock.calculate_pe_ratio(0), 0)

    def test_calculate_volume_weighted_stock_price(self):
        trade1 = Trade(self.common_stock, 10, TradeType.Buy, 15.0, datetime.now() - timedelta(minutes=10))
        trade2 = Trade(self.common_stock, 5, TradeType.Sell, 18.0, datetime.now() - timedelta(minutes=5))
        trades = [trade1, trade2]

        expected_price = (10 * 15.0 + 5 * 18.0) / (10 + 5)
        self.assertAlmostEqual(self.common_stock.calculate_volume_weighted_stock_price(trades), expected_price)

    def test_calculate_volume_weighted_stock_price_no_trades(self):
        self.assertEqual(self.common_stock.calculate_volume_weighted_stock_price([]), 0)

    def test_calculate_gbce_index(self):
        prices = [15.0, 18.0]
        expected_index = (15.0 * 18.0) ** (1 / len(prices))
        self.assertAlmostEqual(Stock.calculate_gbce_index(prices), expected_index)

    def test_calculate_gbce_index_empty_prices(self):
        self.assertEqual(Stock.calculate_gbce_index([]), 0)

    #==============================================================================

    def test_valid_trade_creation(self):
        trade = Trade(stock=self.trade_stock, quantity=100, type=TradeType.Buy, price=20.0)
        self.assertEqual(trade.stock, self.trade_stock)
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.type, TradeType.Buy)
        self.assertEqual(trade.price, 20.0)
        self.assertIsInstance(trade.date, datetime)

    def test_invalid_stock(self):
        with self.assertRaises(ValueError):
            Trade(stock=None, quantity=100, type=TradeType.Buy, price=20.0)

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            Trade(stock=self.trade_stock, quantity=-10, type=TradeType.Buy, price=20.0)

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            Trade(stock=self.trade_stock, quantity=100, type=TradeType.Buy, price=0.0)

    def test_invalid_future_date(self):
        future_date = datetime.now() + timedelta(days=1)
        with self.assertRaises(ValueError):
            Trade(stock=self.trade_stock, quantity=100, type=TradeType.Buy, price=20.0, date=future_date)

if __name__ == '__main__':
    unittest.main()