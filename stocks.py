import yfinance as yf
import pandas as pd
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_stock_data(ticker, start=None, end=None, period='3y', interval='1d'):
    try:
        logging.info(f"Fetching data for {ticker} with start={start}, end={end}, period={period}, interval={interval}")
        stock = yf.Ticker(ticker)
        if start and end:
            print(f"Fetching data for {ticker} from {start} to {end} with interval {interval}")
            print(stock.history(start=start, end=end, interval=interval))
            df = stock.history(start=start, end=end, interval=interval)
        else:
            df = stock.history(period=period, interval=interval)
        
        if df.empty:
            logging.warning(f"No data returned for {ticker} using the specified parameters.")
        else:
            logging.info(f"Successfully fetched {len(df)} rows of data for {ticker}.")
            
        return df
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_daily_returns(df):
    df = df.copy()
    df['Daily_Return'] = df['Close'].pct_change()
    return df

def clean_missing_data(df):
    return df.dropna(subset=['Daily_Return'])

def process_stock_data(df):
    df = calculate_daily_returns(df)
    df = clean_missing_data(df)
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    df['Predicted_Direction'] = df['Daily_Return'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')
    return df