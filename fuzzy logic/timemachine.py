# Final function with test variables

import pandas as pd
from datetime import datetime
import numpy as np


# Function to calculate the time deviation without considering midnight as a reference
def check_user_pattern_deviation(eth_address, new_timestamp):
    # Read the CSV file to get the timestamps for the given Ethereum address
    df = pd.read_csv("ethereum_transactions_modified.csv")
    df_user = df[df['sender_eth_address'] == eth_address]
    
    # If there are no transactions for this address, return a message
    if df_user.empty:
        return "No transactions found for this Ethereum address."
    
    # Convert Unix timestamps to datetime objects for the user's transactions
    df_user['datetime'] = pd.to_datetime(df_user['timestamp'], unit='s')
    
    # Find the earliest transaction time to set as the "start" of the user's day
    earliest_time = df_user['datetime'].min()
    df_user['time_from_earliest'] = (df_user['datetime'] - earliest_time).dt.total_seconds() / 60.0  # convert to minutes
    
    # Calculate the mean and standard deviation for the user's transaction times from the earliest
    mean_time_from_earliest = df_user['time_from_earliest'].mean()
    std_dev_from_earliest = df_user['time_from_earliest'].std() if len(df_user['time_from_earliest']) > 1 else 0
    
    # Convert the new timestamp to datetime
    new_datetime = datetime.utcfromtimestamp(new_timestamp)
    # Calculate the time from the earliest in minutes
    new_time_from_earliest = (new_datetime - earliest_time).total_seconds() / 60.0
    
    # Calculate the deviation in minutes and then as a percentage of the standard deviation
    deviation_minutes = new_time_from_earliest - mean_time_from_earliest
    deviation_percentage = (deviation_minutes / std_dev_from_earliest) * 100 if std_dev_from_earliest > 0 else None
    
    info = {
        'eth_address': eth_address,
        'new_transaction_time': new_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'mean_time_from_earliest_minutes': mean_time_from_earliest,
        'standard_deviation_from_earliest_minutes': std_dev_from_earliest,
        'deviation_minutes': deviation_minutes,
        'deviation_percentage': deviation_percentage
    }

    return round(info['deviation_percentage'])

# Test variables
eth_address_test = '0x50d970f3556dabd44f3569e908ed768293f65dfc'  # The Ethereum address to test
new_timestamp_test = 1612633200  # A specific Unix timestamp to test

# Call the function with the test variables
#test_deviation_info = check_user_pattern_deviation(eth_address_test, new_timestamp_test)
#print(round(test_deviation_info['deviation_percentage']))
