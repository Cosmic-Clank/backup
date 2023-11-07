# Re-examine the extraction code and correct the mistake
import re
import datetime

def extract_data(file_path):
    def extract_all_eth_sendTransaction_v2(file_path):
        transactions = []
        transaction_block = ''
        inside_transaction_block = False

        with open(file_path, 'r') as file:
            for line in file:
                # Detect the start of a transaction block
                if 'eth_sendTransaction' in line:
                    inside_transaction_block = True
                    transaction_block = line  # Start a new transaction block
                elif inside_transaction_block:
                    # If we're in a transaction block, keep adding lines
                    transaction_block += line
                    # If the line starts with a timestamp, we've reached a new log entry
                    if re.match(r'\[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\]', line):
                        inside_transaction_block = False
                        # Add the complete transaction block to the list
                        transactions.append(transaction_block.strip())
                        # Reset the block for the next transaction
                        transaction_block = ''
                # If the next line starts with a new timestamp and we have an open transaction block, close it
                elif transaction_block and re.match(r'\[\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\]', line):
                    transactions.append(transaction_block.strip())
                    transaction_block = ''  # Reset for any subsequent transactions

        # Return the list of transaction blocks
        return transactions

    # Extract all 'eth_sendTransaction' entries with the adjusted function
    newest_log_file_path = "ganache-20231103-134515.log"
    all_eth_sendTransaction_entries_v2 = extract_all_eth_sendTransaction_v2(newest_log_file_path)
    all_eth_sendTransaction_entries_v2

    # Adjust the regex pattern if necessary and extract the details again
    transaction_detail_pattern = re.compile(
        r'"from":\s*"(0x[0-9a-fA-F]+)".*'
        r'"to":\s*"(0x[0-9a-fA-F]+)".*'
        r'"value":\s*"(0x[0-9a-fA-F]+)"',
        re.DOTALL  # The DOTALL flag is used to make the '.' special character match any character at all, including a newline
    )

    timestamp_pattern = re.compile(r'\[(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}:\d{2})\.\d{3}\]')

    # Re-extract details from the first non-zero value transaction block
    transaction_details_match = transaction_detail_pattern.search(all_eth_sendTransaction_entries_v2[1])
    timestamp_match = timestamp_pattern.search(all_eth_sendTransaction_entries_v2[1])

    # Prepare the dictionary to store extracted data
    transaction_details = {}

    if transaction_details_match:
        transaction_details['from'] = transaction_details_match.group(1)
        transaction_details['to'] = transaction_details_match.group(2)
        # Convert the hexadecimal value to decimal
        transaction_details['value'] = int(transaction_details_match.group(3), 16)

    if timestamp_match:
        # Convert the timestamp to a unix timestamp
        transaction_timestamp = datetime.datetime.strptime(timestamp_match.group(1), '%Y/%m/%d %H:%M:%S')
        transaction_details['timestamp'] = int(transaction_timestamp.timestamp())
        
    return transaction_details

print(extract_data("ganache-20231103-134515.log"))
