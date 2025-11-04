import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the cleaned data
df = pd.read_csv('cleaned_and_transformed_data.csv')

# Normalize numerical columns (excluding categorical and date columns)
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
scaler = MinMaxScaler()
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

# Save normalized data
df.to_csv('normalized_business_analytics.csv', index=False)
