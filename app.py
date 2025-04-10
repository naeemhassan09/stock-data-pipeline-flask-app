import database
from flask import Flask, render_template, request
import stocks
import assets
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
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


top_active_stocks = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT', 'NVDA', 'META', 'NFLX', 'AMD', 'BRK-B']
benchmarks = {'S&P 500': 'SPY', 'Gold': 'GLD', 'Silver': 'SLV', 'Oil': 'USO'}

train_start = "2022-01-01"
train_end = "2024-12-31"
test_start = "2025-01-01"
test_end = "2025-03-31"

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    correlation_html = ""
    if request.method == "POST":
        try:
            investment = float(request.form.get("investment", 0))
        except ValueError:
            investment = 0

        # Define date ranges (you can also define these globally)
        train_start = "2022-01-01"
        train_end = "2024-12-31"
        test_start = "2023-01-01"
        test_end = "2023-03-31"

        # --- TRAINING DATA FOR STOCKS (for correlation matrix) ---
        train_data = {}
        for ticker in top_active_stocks:
            table_name = f"stock_train_{ticker}"
            df = None
            if database.table_exists(table_name):
                df = pd.read_sql_table(table_name, database.get_engine())
                if df.empty:
                    df = stocks.fetch_stock_data(ticker, start=train_start, end=train_end)
                    if df is not None:
                        df = stocks.process_stock_data(df)
                        database.store_df_to_db(df, table_name=table_name)
            else:
                df = stocks.fetch_stock_data(ticker, start=train_start, end=train_end)
                if df is not None:
                    df = stocks.process_stock_data(df)
                    database.store_df_to_db(df, table_name=table_name)
            if df is not None:
                train_data[ticker] = df

        returns_dict = {ticker: df['Daily_Return'] for ticker, df in train_data.items() if not df.empty}
        returns_df = pd.DataFrame(returns_dict).dropna()
        correlation_matrix = returns_df.corr()
        correlation_html = correlation_matrix.to_html(classes="table table-striped")

        # --- TEST DATA FOR STOCKS ---
        asset_results = {}
        for ticker in top_active_stocks:
            table_name = f"stock_test_{ticker}"
            df = None
            if database.table_exists(table_name):
                df = pd.read_sql_table(table_name, database.get_engine())
                if df.empty:
                    df = stocks.fetch_stock_data(ticker, start=test_start, end=test_end)
                    if df is not None:
                        df = stocks.process_stock_data(df)
                        database.store_df_to_db(df, table_name=table_name)
            else:
                df = stocks.fetch_stock_data(ticker, start=test_start, end=test_end)
                if df is not None:
                    df = stocks.process_stock_data(df)
                    database.store_df_to_db(df, table_name=table_name)
            if df is not None and not df.empty:
                cum_ret = df['Cumulative_Return'].iloc[-1]
                predicted_value = investment * (1 + cum_ret)
                asset_results[ticker] = {"Cumulative_Return": cum_ret, "Predicted_Value": predicted_value}

        # --- TEST DATA FOR BENCHMARK ASSETS ---
        for name, ticker in benchmarks.items():
            table_name = f"asset_test_{name}"
            df = None
            if database.table_exists(table_name):
                df = pd.read_sql_table(table_name, database.get_engine())
                if df.empty:
                    df = assets.fetch_asset_data(ticker, start=test_start, end=test_end)
                    if df is not None:
                        df = assets.process_asset_data(df)
                        database.store_df_to_db(df, table_name=table_name)
            else:
                df = assets.fetch_asset_data(ticker, start=test_start, end=test_end)
                if df is not None:
                    df = assets.process_asset_data(df)
                    database.store_df_to_db(df, table_name=table_name)
            if df is not None and not df.empty:
                cum_ret = df['Cumulative_Return'].iloc[-1]
                predicted_value = investment * (1 + cum_ret)
                asset_results[name] = {"Cumulative_Return": cum_ret, "Predicted_Value": predicted_value}

        results = asset_results

    return render_template("index.html", results=results, correlation_html=correlation_html)
if __name__ == "__main__":
    test_db_connection()
    app.run(host="0.0.0.0", port=8080, debug=True)