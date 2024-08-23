import pandas as pd
import numpy as np

data_set = pd.read_csv('AI Research & Development Fellowship - Assessment Datasets - Question  4 - Data Manipulation.csv')

data_set['transaction_date'] = pd.to_datetime(data_set['transaction_date'])
data_set['Year'] = data_set['transaction_date'].dt.year
aggregated_data = data_set.groupby(['user_id', 'Year', 'category'])['amount'].sum().reset_index()

annual_spending = aggregated_data.groupby(['user_id', 'Year'])['amount'].sum().reset_index()

avg_annual_spending = annual_spending.groupby('user_id')['amount'].mean().reset_index()
qualifying_spenders = avg_annual_spending[avg_annual_spending['amount'] >= 1000]['user_id']

filtered_data = annual_spending[annual_spending['user_id'].isin(qualifying_spenders)]
pivot_data = filtered_data.pivot(index='user_id', columns='Year', values='amount')

# Fill NaN with a marker value (e.g., np.nan) that indicates no spending for the year
pivot_data = pivot_data.fillna(np.nan)

# Apply percentage change calculation only where valid (more than one year with non-zero spending)
pivot_data['percentage change'] = pivot_data.apply(
    lambda x: ((x.max() - x.min()) / x.min() * 100)
    if x.min() > 0 and len(x.dropna().unique()) > 1 else None,
    axis=1
)

# Display results
print("original data set:", data_set)
print("aggregated data:",aggregated_data)
print("annual spending:",annual_spending)
print("average annual spending:",avg_annual_spending)
print("highest spenders:",qualifying_spenders)
print("filtered df:",filtered_data)
print("pivot:",pivot_data[['percentage change']])
