"""
This module fetches historical cryptocurrency data from Binance and processes it into a pandas DataFrame.
"""

import time
import datetime
import pandas as pd
import requests

# Convert a date to a Unix timestamp in milliseconds
def date_to_milliseconds(date_str):
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return int(dt.timestamp() * 1000)

def get_historical_binance_data(symbol='BTCUSDT', time_interval='1h', start_time=None, limit=1000):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': time_interval,  # Updated parameter name
        'limit': limit
    }
    if start_time:
        params['startTime'] = start_time
    
    response = requests.get(url, params=params, timeout=10)  # Added timeout of 10 seconds
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
        utc_time = datetime.datetime.fromtimestamp(new_timestamp / 1000, datetime.UTC)
        print(f"Fetching data starting from: {utc_time}")

        # Fetch data (start from the earliest timestamp or beginning)
        new_data = get_historical_binance_data(symbol=symbol, time_interval=interval, start_time=new_timestamp)

        if new_data.empty:
            print("No more data to fetch.")
            break

        # Update the last timestamp to fetch the next batch of data
        new_timestamp = int(new_data['timestamp'].iloc[-1].timestamp() * 1000)
        if not all_data.empty:
            existing_timestamp = int(all_data['timestamp'].iloc[-1].timestamp() * 1000)

        if existing_timestamp == new_timestamp:
            return all_data
        
        # firs time
        if all_data.empty:
            all_data = pd.concat([all_data, new_data])
        else:
            all_data = pd.concat([all_data, new_data[1:]])
        # Sleep to avoid hitting rate limits
        time.sleep(1)

    return all_data

if __name__ == '__main__':
    # Get all historical BTC 1-hour candle data starting from August 17, 2017
        intervals = ['1h', '2h', '4h', '12h', '1d']
        # intervals = ['1d']
        for interval in intervals:
            btc_historical_data = gather_all_historical_data(interval=interval, start_date='2017-08-16')

            # Save the DataFrame to a CSV file
            btc_historical_data.to_csv(f'./data/btc_all_{interval}_candles_from_2017.csv', index=False)

            print(f"Data collection for {interval} complete!")