import database
from flask import Flask, render_template, request
import stocks
import assets
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def test_db_connection():
    engine = database.get_engine()
    try:
        conn = engine.connect()
        print("Successfully connected to PostgreSQL database.")
        conn.close()
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)
    finally:
        engine.dispose()

# Global constants
top_active_stocks = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT', 'NVDA', 'META', 'NFLX', 'AMD', 'BRK-B']
benchmarks = {'S&P 500': 'SPY', 'Gold': 'GLD', 'Silver': 'SLV', 'Oil': 'USO'}

# Date ranges for training and test data
TRAIN_START = "2022-01-01"
TRAIN_END = "2024-12-31"
TEST_START = "2023-01-01"
TEST_END = "2023-03-31"

def get_training_data():
    """Fetches or loads training data for top active stocks used for correlation matrix and optimization."""
    train_data = {}
    for ticker in top_active_stocks:
        table_name = f"stock_train_{ticker}"
        df = None
        if database.table_exists(table_name):
            df = pd.read_sql_table(table_name, database.get_engine())
            if df.empty:
                df = stocks.fetch_stock_data(ticker, start=TRAIN_START, end=TRAIN_END)
                if df is not None:
                    df = stocks.process_stock_data(df)
                    database.store_df_to_db(df, table_name=table_name)
        else:
            df = stocks.fetch_stock_data(ticker, start=TRAIN_START, end=TRAIN_END)
            if df is not None:
                df = stocks.process_stock_data(df)
                database.store_df_to_db(df, table_name=table_name)
        if df is not None:
            train_data[ticker] = df
    return train_data

def build_correlation_html(train_data):
    """Builds an HTML table of the correlation matrix from training data."""
    returns_dict = {ticker: df['Daily_Return'] for ticker, df in train_data.items() if not df.empty}
    if returns_dict:
        returns_df = pd.DataFrame(returns_dict).dropna()
        corr_matrix = returns_df.corr()
        return corr_matrix.to_html(classes="table table-striped")
    else:
        return "<p>No training data available for correlation matrix.</p>"

def get_test_data(investment):
    """
    Fetches or loads test data for both stocks and benchmark assets.
    Returns a tuple of:
      - asset_results: Dictionary of individual asset predictions.
      - test_data_store: Dictionary storing the DataFrame for each asset.
    """
    asset_results = {}
    test_data_store = {}
    
    # Process stocks test data
    for ticker in top_active_stocks:
        table_name = f"stock_test_{ticker}"
        df = None
        if database.table_exists(table_name):
            df = pd.read_sql_table(table_name, database.get_engine())
            if df.empty:
                df = stocks.fetch_stock_data(ticker, start=TEST_START, end=TEST_END)
                if df is not None:
                    df = stocks.process_stock_data(df)
                    database.store_df_to_db(df, table_name=table_name)
        else:
            df = stocks.fetch_stock_data(ticker, start=TEST_START, end=TEST_END)
            if df is not None:
                df = stocks.process_stock_data(df)
                database.store_df_to_db(df, table_name=table_name)
        if df is not None and not df.empty:
            cum_ret = df['Cumulative_Return'].iloc[-1]
            predicted_value = investment * (1 + cum_ret)
            asset_results[ticker] = {"Cumulative_Return": cum_ret, "Predicted_Value": predicted_value}
            test_data_store[ticker] = df

    # Process benchmark assets test data
    for name, ticker in benchmarks.items():
        table_name = f"asset_test_{name}"
        df = None
        if database.table_exists(table_name):
            df = pd.read_sql_table(table_name, database.get_engine())
            if df.empty:
                df = assets.fetch_asset_data(ticker, start=TEST_START, end=TEST_END)
                if df is not None:
                    df = assets.process_asset_data(df)
                    database.store_df_to_db(df, table_name=table_name)
        else:
            df = assets.fetch_asset_data(ticker, start=TEST_START, end=TEST_END)
            if df is not None:
                df = assets.process_asset_data(df)
                database.store_df_to_db(df, table_name=table_name)
        if df is not None and not df.empty:
            cum_ret = df['Cumulative_Return'].iloc[-1]
            predicted_value = investment * (1 + cum_ret)
            asset_results[name] = {"Cumulative_Return": cum_ret, "Predicted_Value": predicted_value}
            test_data_store[name] = df

    return asset_results, test_data_store

def calculate_portfolio_metrics(test_data_store, asset_results, investment):
    """
    Calculates a balanced portfolio using equal weighting for assets with positive cumulative returns.
    Returns:
      - portfolio_result: Dictionary with portfolio cumulative return and predicted value.
      - portfolio_metrics: Dictionary with average daily return, volatility, and Sharpe ratio.
      - portfolio_assets: List of asset names included.
    """
    portfolio_result = {}
    portfolio_metrics = {}
    positive_assets = {asset: data for asset, data in asset_results.items() if data["Cumulative_Return"] > 0}
    portfolio_assets = list(positive_assets.keys())
    
    if positive_assets:
        portfolio_dfs = []
        for asset in positive_assets:
            if asset in test_data_store:
                temp_df = test_data_store[asset][['Daily_Return']].rename(columns={'Daily_Return': asset})
                portfolio_dfs.append(temp_df)
        if portfolio_dfs:
            combined_returns = pd.concat(portfolio_dfs, axis=1, join='inner')
            portfolio_daily_return = combined_returns.mean(axis=1)
            portfolio_avg_daily_return = portfolio_daily_return.mean()
            portfolio_volatility = portfolio_daily_return.std()
            sharpe_ratio = (portfolio_avg_daily_return / portfolio_volatility) if portfolio_volatility != 0 else None
            portfolio_cumulative_return = (1 + portfolio_daily_return).prod() - 1
            portfolio_predicted_value = investment * (1 + portfolio_cumulative_return)
            portfolio_result = {
                "Portfolio_Cumulative_Return": portfolio_cumulative_return,
                "Portfolio_Predicted_Value": portfolio_predicted_value
            }
            portfolio_metrics = {
                "Average Daily Return": portfolio_avg_daily_return,
                "Volatility": portfolio_volatility,
                "Sharpe Ratio": sharpe_ratio
            }
    return portfolio_result, portfolio_metrics, portfolio_assets

def calculate_optimized_portfolio(investment, train_data, asset_results):
    """
    A basic optimization that uses training data to compute weights proportional to an asset's 
    average daily return as a proxy for its historical performance.
    
    Returns:
      - optimized_predicted_value: The predicted portfolio value using optimized weights.
      - optimized_cum_ret: The weighted average cumulative return.
      - portfolio_composition: A dictionary with each asset's allocation percentage.
    """
    weights = {}
    total_avg_return = 0.0
    positive_assets = [asset for asset, data in asset_results.items() if data["Cumulative_Return"] > 0]
    
    # Use training data to compute average daily return for each asset
    for asset in positive_assets:
        if asset in train_data and not train_data[asset].empty:
            avg_return = train_data[asset]['Daily_Return'].mean()
            if avg_return > 0:
                weights[asset] = avg_return
                total_avg_return += avg_return
    
    portfolio_composition = {}
    if total_avg_return > 0:
        for asset, ret in weights.items():
            portfolio_composition[asset] = round(ret / total_avg_return * 100, 2)  # allocation in %
    
    optimized_predicted_value = 0.0
    for asset, alloc_percent in portfolio_composition.items():
        weight = alloc_percent / 100.0
        if asset in asset_results:
            optimized_predicted_value += investment * weight * (1 + asset_results[asset]['Cumulative_Return'])
    
    optimized_cum_ret = sum((alloc_percent / 100.0) * asset_results[asset]['Cumulative_Return']
                              for asset, alloc_percent in portfolio_composition.items())
    
    return optimized_predicted_value, optimized_cum_ret, portfolio_composition

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    correlation_html = ""
    portfolio_result = {}
    portfolio_metrics = {}
    portfolio_assets = []
    portfolio_composition = {}
    optimized_portfolio = {}
    optimized_metrics = {}
    
    if request.method == "POST":
        try:
            investment = float(request.form.get("investment", 0))
        except ValueError:
            investment = 0
        
        # --- TRAINING DATA for Correlation Matrix and Optimization ---
        train_data = get_training_data()
        correlation_html = build_correlation_html(train_data)
        
        # --- TEST DATA for Individual Predictions ---
        asset_results, test_data_store = get_test_data(investment)
        results = asset_results
        
        # --- Equal-Weighted Portfolio Calculation & Additional Metrics ---
        portfolio_result, portfolio_metrics, portfolio_assets = calculate_portfolio_metrics(test_data_store, asset_results, investment)
        
        # Equal allocation composition (if any assets qualify)
        if portfolio_assets:
            portfolio_composition = {asset: round(100.0 / len(portfolio_assets), 2) for asset in portfolio_assets}
        
        # --- Optimized Portfolio Based on Training Data ---
        optimized_predicted_value, optimized_cum_ret, optimized_composition = calculate_optimized_portfolio(investment, train_data, asset_results)
        optimized_portfolio = {
            "Portfolio_Cumulative_Return": optimized_cum_ret,
            "Portfolio_Predicted_Value": optimized_predicted_value
        }
    
    return render_template("index.html", results=results, correlation_html=correlation_html,
                           portfolio=portfolio_result, metrics=portfolio_metrics,
                           portfolio_assets=portfolio_assets, portfolio_composition=portfolio_composition,
                           optimized_portfolio=optimized_portfolio, optimized_composition=optimized_composition)

if __name__ == "__main__":
    test_db_connection()
    app.run(host="0.0.0.0", port=8080, debug=True)