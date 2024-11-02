import pandas as pd

# Load the CSV file
fname = input("csv: ")
df = pd.read_csv(fname)

# Separate the 'organs' column from the rest of the DataFrame
organs_column = df['organs']  # Keep the 'organs' column

# Drop the 'organs' column from the DataFrame to prepare for transposition
df_numeric = df.drop(columns='organs')

# Transpose the numeric DataFrame
df_transposed = df_numeric.T

# Add 'organs' as the first row (column headers)
df_transposed.columns = organs_column.values

# Reset the index to create a new DataFrame
df_transposed.reset_index(inplace=True)

# Rename the first column to 'organs'
df_transposed.rename(columns={'index': 'organs'}, inplace=True)

filename = f'transformed_{fname.strip(".csv")}.csv'
# Save the transformed DataFrame back to a new CSV file
df_transposed.to_csv(filename, encoding='utf-8-sig', index=False)
