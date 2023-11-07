import pandas as pd
from scipy import stats


def ether_analyzer(sender_address, transaction_value):

    sender_address = "0x50d970f3556dabd44f3569e908ed768293f65dfc"
    transaction_value = 300
    # Load the dataset for the specified sender address
    df_transactions = pd.read_csv('ethereum_transactions_modified.csv')
    df_sender_transactions = df_transactions[df_transactions['sender_eth_address'] == sender_address]
    
    # Check if there are transactions for the given sender address
    if df_sender_transactions.empty:
        return "No transactions found for this Ethereum address."
    
    # Ensure 'ether_value' column is numeric
    df_sender_transactions['ether_value'] = pd.to_numeric(df_sender_transactions['ether_value'], errors='coerce')
    
    # Remove any rows where 'ether_value' could not be converted to numeric
    df_sender_transactions = df_sender_transactions.dropna(subset=['ether_value'])
    
    # Calculate the Z-score for the 'ether_value' column for the sender's transactions
    df_sender_transactions['z_score'] = stats.zscore(df_sender_transactions['ether_value'])
    
    # Define a threshold for the Z-score to identify high-value outliers
    threshold = 3
    # Check if the provided transaction value is an outlier based on the Z-score
    transaction_z_score = (transaction_value - df_sender_transactions['ether_value'].mean()) / df_sender_transactions['ether_value'].std()
    is_outlier = transaction_z_score > threshold
    
    # Calculate the 97th percentile value to find the biggest number under it for the sender's transactions
    percentile_97_value = df_sender_transactions['ether_value'].quantile(0.97)
    # The largest value under the 97th percentile
    max_value_under_97_percentile = df_sender_transactions[df_sender_transactions['ether_value'] < percentile_97_value]['ether_value'].max()
    
    # Check if the provided transaction value is among the top 3% outliers
    is_top_3_percent_outlier = transaction_value > percentile_97_value
    # Calculate the deviation from the max value under the 97th percentile if it's an outlier
    deviation_from_max_under_97 = transaction_value - max_value_under_97_percentile if is_top_3_percent_outlier else 0
    # Calculate the percentage of deviation from that maximum value under the 97th percentile
    percent_deviation_from_max_under_97 = (deviation_from_max_under_97 / max_value_under_97_percentile) * 100 if is_top_3_percent_outlier else 0
    
    result =  {
        'sender_address': sender_address,
        'transaction_value': transaction_value,
        'is_outlier_based_on_z_score': is_outlier,
        'transaction_z_score': transaction_z_score,
        'is_top_3_percent_outlier': is_top_3_percent_outlier,
        'deviation_from_max_under_97': deviation_from_max_under_97,
        'percent_deviation_from_max_under_97': percent_deviation_from_max_under_97
    }

    return round(result['percent_deviation_from_max_under_97'])
