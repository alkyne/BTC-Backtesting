import pandas as pd
import requests
import time
import datetime

# Convert a date to a Unix timestamp in milliseconds
def date_to_milliseconds(date_str):
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return int(dt.timestamp() * 1000)

def get_historical_binance_data(symbol='BTCUSDT', interval='1h', start_time=None, limit=1000):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    if start_time:
        params['startTime'] = start_time
    
    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])

    # Convert timestamp to readable datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Drop unnecessary columns
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    # Convert price and volume columns to numeric types
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)

    return df

def gather_all_historical_data(symbol='BTCUSDT', interval='1h', start_date='2017-08-17'):
    all_data = pd.DataFrame()
    new_timestamp = date_to_milliseconds(start_date)  # Start from the specified date
    existing_timestamp = 0

    while True:
        # Using timezone-aware datetime
        utc_time = datetime.datetime.fromtimestamp(new_timestamp, datetime.UTC)
        print(f"Fetching data starting from: {utc_time}")

        # Fetch data (start from the earliest timestamp or beginning)
        new_data = get_historical_binance_data(symbol=symbol, interval=interval, start_time=new_timestamp)

        if new_data.empty:
            print("No more data to fetch.")
            break

        # Append new data to the existing data

        # Update the last timestamp to fetch the next batch of data
        new_timestamp = int(new_data['timestamp'].iloc[-1].timestamp() * 1000)
        if not all_data.empty:
            existing_timestamp = int(all_data['timestamp'].iloc[-1].timestamp() * 1000)

        if existing_timestamp == new_timestamp:
            return all_data

        all_data = pd.concat([all_data, new_data])
        # Sleep to avoid hitting rate limits
        time.sleep(1)

    return all_data

# Get all historical BTC 1-hour candle data starting from August 17, 2017
btc_historical_data = gather_all_historical_data(start_date='2017-08-17')

# Save the DataFrame to a CSV file
btc_historical_data.to_csv('btc_all_1h_candles_from_2017.csv', index=False)

print("Data collection complete!")