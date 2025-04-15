# This is a test file for the stock data pipeline. it is created using AI help to save the developer time.
import unittest
import pandas as pd
import numpy as np
from stocks import fetch_stock_data, calculate_daily_returns, clean_missing_data, process_stock_data

class TestStockDataPipeline(unittest.TestCase):
    def setUp(self):
        # Create a simple DataFrame for testing transformation functions
        self.sample_data = pd.DataFrame({
            'Close': [100, 105, 110, 108]
        })
    
    def test_calculate_daily_returns(self):
        # Test that calculate_daily_returns computes the correct percentage changes.
        df_returns = calculate_daily_returns(self.sample_data)
        # First row should be NaN
        self.assertTrue(np.isnan(df_returns['Daily_Return'].iloc[0]))
        # Second row: (105 - 100)/100 = 0.05
        self.assertAlmostEqual(df_returns['Daily_Return'].iloc[1], 0.05, places=4)
        # Third row: (110 - 105)/105 ≈ 0.04762
        self.assertAlmostEqual(df_returns['Daily_Return'].iloc[2], 0.04762, places=4)
        # Fourth row: (108 - 110)/110 = -0.01818
        self.assertAlmostEqual(df_returns['Daily_Return'].iloc[3], -0.01818, places=4)

    def test_clean_missing_data(self):
        # After computing daily returns, the first row is NaN
        df_returns = calculate_daily_returns(self.sample_data)
        df_clean = clean_missing_data(df_returns)
        # The cleaned DataFrame should have one less row than the original.
        self.assertEqual(len(df_clean), len(self.sample_data)-1)
        # Ensure no NaN values remain in the 'Daily_Return' column.
        self.assertFalse(df_clean['Daily_Return'].isna().any())
    
    def test_process_stock_data(self):
        # Process sample data and check that required columns are added.
        processed_df = process_stock_data(self.sample_data)
        self.assertIn('Cumulative_Return', processed_df.columns)
        self.assertIn('Predicted_Direction', processed_df.columns)
        # Check that the predicted direction for the second row (return 0.05) is "Increase"
        self.assertEqual(processed_df['Predicted_Direction'].iloc[1], 'Increase')
    
    def test_fetch_stock_data(self):
        # Test fetching actual data; this requires an internet connection.
        df = fetch_stock_data('AAPL', period='1mo', interval='1d')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        # Optionally, verify that the DataFrame contains expected columns.
        self.assertIn('Close', df.columns)

if __name__ == '__main__':
    unittest.main()