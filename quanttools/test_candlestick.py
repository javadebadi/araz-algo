import unittest
from candlestick import Candlestick

class TestCandlestick(unittest.TestCase):

    def test_init(self):
        c = Candlestick()
        self.assertEqual(c._open_, None)
        self.assertEqual(c._high, None)
        self.assertEqual(c._low, None)
        self.assertEqual(c._close, None)
        c = Candlestick(1, 2, 0, 1.5)
        self.assertEqual(c._open_, 1)
        self.assertEqual(c._high, 2)
        self.assertEqual(c._low, 0)
        self.assertEqual(c._close, 1.5)
        self.assertEqual(c._sorted_ohlc, [0, 1, 1.5, 2])

    def test_property_getter(self):
        c = Candlestick(1, 2, 0, 1.5)
        self.assertEqual(c.open_, 1)
        self.assertEqual(c.high, 2)
        self.assertEqual(c.low, 0)
        self.assertEqual(c.close, 1.5)
        self.assertEqual(c.sorted_ohlc, [0, 1, 1.5, 2])

    def test_set_ohlc(self):
        c = Candlestick()
        with self.assertRaises(TypeError):
            c.set_ohlc('1', 2, 0, 1.5)
        with self.assertRaises(TypeError):
            c.set_ohlc(1, '2', 0, 1.5)
        with self.assertRaises(TypeError):
            c.set_ohlc(1, 2, '0', 1.5)
        with self.assertRaises(TypeError):
            c.set_ohlc(1, 2, 0, '1.5')
        with self.assertRaises(AssertionError):
            # low is bigger than high
            c.set_ohlc(open_=5, high=10, low=20, close=5)
        with self.assertRaises(AssertionError):
            # low is bigger than close
            c.set_ohlc(open_=9, high=10, low=6, close=5)
        with self.assertRaises(AssertionError):
            # low is bigger than open
            c.set_ohlc(open_=5, high=10, low=6, close=9)
        with self.assertRaises(AssertionError):
            # high is smaller than close
            c.set_ohlc(open_=5, high=10, low=6, close=50)
        with self.assertRaises(AssertionError):
            # high is smaller than open
            c.set_ohlc(open_=50, high=10, low=6, close=9)

    
    def test_len(self):
        c = Candlestick(100, 200, 0, 150)
        self.assertEqual(len(c), 200)

    def test_upper_shadow(self):
        c = Candlestick(100, 550, 0, 150)
        self.assertEqual(c.upper_shadow, 400)

    def test_lower_shadow(self):
        c = Candlestick(100, 550, 0, 150)
        self.assertEqual(c.lower_shadow, 100)

    def test_real_body(self):
        c = Candlestick(100, 550, 0, 150)
        self.assertEqual(c.real_body, 50)

    def test_is_hollow(self):
        c = Candlestick(100, 550, 0, 150)
        self.assertEqual(c.is_hollow, True)
        c = Candlestick(500, 550, 0, 250)
        self.assertEqual(c.is_hollow, False)

    def test_is_filled(self):
        c = Candlestick(100, 550, 0, 150)
        self.assertEqual(c.is_filled, False)
        c = Candlestick(500, 550, 0, 250)
        self.assertEqual(c.is_filled, True)

    def test_operator_overloading_trudiv(self):
        c = Candlestick(100, 500, 0, 50)
        d = Candlestick(1000, 5000, 0, 500)
        self.assertEqual(d / c, 10.0)
        self.assertEqual(c / d, 0.1)
    
if __name__ == '__main__':
    unittest.main()