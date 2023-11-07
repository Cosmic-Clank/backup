import pandas as pd

# Load the dataset
df = pd.read_csv('dataset.csv')

# Shuffle the dataset
df_shuffled = df.sample(frac=1).reset_index(drop=True)

# Save the shuffled dataset to a new CSV file
df_shuffled.to_csv('dataset.csv', index=False)