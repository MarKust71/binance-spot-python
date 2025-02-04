# helpers/tests/test_fetch_candles.py
"""
Fetch candles test module.
"""


import unittest
from unittest.mock import patch
import pandas as pd
from helpers.fetch_candles import fetch_candles

class TestFetchCandles(unittest.TestCase):
    """
    This class represents a simple example class.

    Attributes:
    """

    @patch('helpers.fetch_candles.client.get_klines')
    def test_fetch_candles_success(self, mock_get_klines) -> None:
        """
        This function does something.

        Args:
            self: Description of param1.
            mock_get_klines: Description of param1.

        Returns:
            None
        """
        # Mock data
        mock_get_klines.return_value = [
            [1609459200000, "29000.0", "29500.0", "28500.0", "29000.0", "1000",
             1609462800000, "29000000", 100, "500", "14500000", "0"]
        ]

        result = fetch_candles('BTCUSDT', '1h', 1, end_time=None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result['timestamp'][0], pd.to_datetime(1609459200000, unit='ms'))
        self.assertEqual(result['close'][0], 29000.0)

    @patch('helpers.fetch_candles.client.get_klines')
    def test_fetch_candles_failure(self, mock_get_klines) -> None:
        """
        This function does something.

        Args:
            self: Description of param1.
            mock_get_klines: Description of param1.

        Returns:
            None
        """
        # Simulate an exception
        mock_get_klines.side_effect = Exception("API error")

        result = fetch_candles('BTCUSDT', '1h', 1, end_time=None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
