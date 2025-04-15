# This is a test module for the app.py file.
# The following unit tests were generated with the help of AI.
# This approach streamlined the process, ensured comprehensive coverage
# of critical functions (such as correlation calculations and portfolio metrics),
# and allowed more time to focus on integrating and refining the overall system.
# The tests are designed to validate the functionality of the app module,

import unittest
import pandas as pd
import numpy as np

# Import the functions to be tested from your app module.
# Adjust the module name if needed.
from app import (
    build_correlation_html,
    build_combined_correlation_html,
    compute_group_metrics,
    calculate_portfolio_metrics,
    calculate_optimized_portfolio
)

class TestAppFunctions(unittest.TestCase):
    def setUp(self):
        # Create dummy training data for stocks.
        # For each asset, we simulate a DataFrame with a 'Daily_Return' column.
        self.df_A = pd.DataFrame({
            'Daily_Return': [0.01, 0.02, 0.015, -0.005, 0.01]
        })
        self.df_A['Cumulative_Return'] = (1 + self.df_A['Daily_Return']).cumprod() - 1

        self.df_B = pd.DataFrame({
            'Daily_Return': [0.02, -0.01, 0.005, 0.01, 0.015]
        })
        self.df_B['Cumulative_Return'] = (1 + self.df_B['Daily_Return']).cumprod() - 1

        # Create dummy training data dictionaries
        self.train_data = {'A': self.df_A, 'B': self.df_B}
        # For combined correlation, also create dummy benchmark data (similar structure)
        self.bench_data = {'Benchmark1': self.df_A, 'Benchmark2': self.df_B}

        # Create dummy asset_results for test data.
        # Asset "A" has a positive cumulative return, and "B" has a negative one.
        self.asset_results = {
            'A': {"Cumulative_Return": 0.10, "Predicted_Value": 1100},
            'B': {"Cumulative_Return": -0.05, "Predicted_Value": 950}
        }

        # Dummy test_data_store contains DataFrames for each asset.
        self.test_data_store = {
            'A': self.df_A,
            'B': self.df_B
        }

        # Use a fixed investment for testing.
        self.investment = 1000

    def test_build_correlation_html(self):
        # Test that build_correlation_html returns an HTML table string.
        html = build_correlation_html(self.train_data)
        self.assertIsInstance(html, str)
        self.assertIn("<table", html)

    def test_build_combined_correlation_html(self):
        # Test combined correlation that uses both stocks and benchmark training data.
        html = build_combined_correlation_html(self.train_data, self.bench_data)
        self.assertIsInstance(html, str)
        self.assertIn("<table", html)

    def test_compute_group_metrics(self):
        # Test compute_group_metrics returns metrics and group average dictionaries.
        metrics, group_avg = compute_group_metrics(self.train_data)
        self.assertTrue('A' in metrics)
        self.assertTrue('B' in metrics)
        self.assertIsInstance(group_avg, dict)
        # Check that the group average contains expected keys.
        self.assertIn("Average Daily Return", group_avg)
        self.assertIn("Volatility", group_avg)
        self.assertIn("Cumulative Return", group_avg)

    def test_calculate_portfolio_metrics(self):
        # Only asset A should be included because B has a negative cumulative return.
        portfolio_result, portfolio_metrics, portfolio_assets = calculate_portfolio_metrics(
            self.test_data_store, self.asset_results, self.investment
        )
        self.assertIn('A', portfolio_assets)
        self.assertNotIn('B', portfolio_assets)
        self.assertEqual(len(portfolio_assets), 1)
        self.assertIn("Portfolio_Cumulative_Return", portfolio_result)
        self.assertIn("Portfolio_Predicted_Value", portfolio_result)

    def test_calculate_optimized_portfolio(self):
        # Test the optimized portfolio function. With our dummy data, asset B is excluded due to negative return.
        optimized_predicted_value, optimized_cum_ret, optimized_composition = calculate_optimized_portfolio(
            self.investment, self.train_data, self.asset_results
        )
        # Expect that only asset A is included and allocated 100%
        self.assertIn('A', optimized_composition)
        self.assertNotIn('B', optimized_composition)
        self.assertEqual(optimized_composition['A'], 100.0)
        # Optionally, check that optimized_predicted_value is calculated reasonably.
        self.assertGreater(optimized_predicted_value, self.investment)

if __name__ == '__main__':
    # These tests were generated with the help of AI to speed up development while ensuring robust testing
    unittest.main()