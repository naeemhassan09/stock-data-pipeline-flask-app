# The following unit tests were generated with the help of AI.
# This approach streamlined the process, ensured comprehensive coverage
# of critical functions (such as daily return calculations and data cleaning),
# and allowed more time to focus on integrating and refining the overall system.
import unittest
import pandas as pd
import numpy as np
from assets import fetch_asset_data, calculate_daily_returns, clean_missing_data, process_asset_data

class TestAssetDataPipeline(unittest.TestCase):
    def setUp(self):
        # Create a simple DataFrame for testing transformation functions
        self.sample_data = pd.DataFrame({
            'Close': [50, 55, 60, 58]
        })
    
    def test_calculate_daily_returns(self):
        # Calculate daily returns for the sample data
        df_returns = calculate_daily_returns(self.sample_data)
        # The first row should be NaN since there's no previous value to compare.
        self.assertTrue(np.isnan(df_returns['Daily_Return'].iloc[0]))
        # Second row: (55 - 50)/50 = 0.1
        self.assertAlmostEqual(df_returns['Daily_Return'].iloc[1], 0.1, places=4)
        # Third row: (60 - 55)/55 ≈ 0.090909
        self.assertAlmostEqual(df_returns['Daily_Return'].iloc[2], 0.090909, places=4)
        # Fourth row: (58 - 60)/60 ≈ -0.033333
        self.assertAlmostEqual(df_returns['Daily_Return'].iloc[3], -0.033333, places=4)
    
    def test_clean_missing_data(self):
        # After calculating daily returns, the first row is NaN.
        df_returns = calculate_daily_returns(self.sample_data)
        df_clean = clean_missing_data(df_returns)
        # The cleaned DataFrame should have one fewer row.
        self.assertEqual(len(df_clean), len(self.sample_data) - 1)
        # Ensure there are no NaN values remaining in the 'Daily_Return' column.
        self.assertFalse(df_clean['Daily_Return'].isna().any())
    
    def test_process_asset_data(self):
        # Process sample data and check that the required columns are added.
        processed_df = process_asset_data(self.sample_data)
        self.assertIn('Cumulative_Return', processed_df.columns)
        self.assertIn('Predicted_Direction', processed_df.columns)
        # Check that for the second row (with a return of 0.1), the predicted direction is "Increase"
        self.assertEqual(processed_df['Predicted_Direction'].iloc[1], 'Increase')
    
    def test_fetch_asset_data(self):
        # This test uses the fetch_asset_data function to retrieve data from Yahoo Finance.
        # It requires an internet connection. Here we use "GLD" (Gold ETF) as an example.
        df = fetch_asset_data("GLD", period="1mo", interval="1d")
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        # Verify that the expected columns exist.
        self.assertIn("Close", df.columns)

if __name__ == '__main__':
    unittest.main()