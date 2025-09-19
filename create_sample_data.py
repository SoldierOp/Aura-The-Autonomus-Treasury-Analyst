import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
np.random.seed(42)
random.seed(42)

# Create sample transactions data
transactions_data = []
base_date = datetime.now() - timedelta(days=90)

# Revenue transactions
for i in range(20):
    date = base_date + timedelta(days=random.randint(0, 90))
    amount = random.uniform(10000, 150000)
    transactions_data.append({
        'Date': date,
        'Description': f'Revenue Transaction {i+1}',
        'Category': 'Revenue',
        'Amount': amount
    })

# Marketing expenses
for i in range(15):
    date = base_date + timedelta(days=random.randint(0, 90))
    amount = -random.uniform(2000, 15000)
    transactions_data.append({
        'Date': date,
        'Description': f'Marketing Campaign {i+1}',
        'Category': 'Marketing',
        'Amount': amount
    })

# Operations expenses
for i in range(25):
    date = base_date + timedelta(days=random.randint(0, 90))
    amount = -random.uniform(500, 5000)
    transactions_data.append({
        'Date': date,
        'Description': f'Operations Expense {i+1}',
        'Category': 'Operations',
        'Amount': amount
    })

transactions_df = pd.DataFrame(transactions_data)
transactions_df = transactions_df.sort_values('Date')

# Create sample campaign data
campaign_data = []
campaign_start = datetime.now() - timedelta(days=30)

# Historical campaigns (normal CAC)
for i in range(20):
    timestamp = campaign_start + timedelta(hours=random.randint(0, 720))
    channel = random.choice(['Adwords', 'Facebook', 'LinkedIn'])
    
    # Normal CAC range
    if channel == 'Adwords':
        spend = random.uniform(1000, 5000)
        acquisitions = random.randint(20, 100)
    else:
        spend = random.uniform(500, 3000)
        acquisitions = random.randint(10, 50)
    
    campaign_data.append({
        'Timestamp': timestamp,
        'Campaign_ID': f'CAMP_{i+1:03d}',
        'Channel': channel,
        'Spend': spend,
        'Acquisitions': acquisitions
    })

# Recent campaigns with high CAC (to trigger alert)
recent_start = datetime.now() - timedelta(hours=48)
for i in range(5):
    timestamp = recent_start + timedelta(hours=random.randint(0, 48))
    spend = random.uniform(2000, 8000)
    acquisitions = random.randint(5, 20)  # Low acquisitions = high CAC
    
    campaign_data.append({
        'Timestamp': timestamp,
        'Campaign_ID': f'CAMP_RECENT_{i+1:03d}',
        'Channel': 'Adwords',
        'Spend': spend,
        'Acquisitions': acquisitions
    })

campaign_df = pd.DataFrame(campaign_data)
campaign_df = campaign_df.sort_values('Timestamp')

# Create targets data
targets_data = [
    {'Metric_Name': 'Current_Cash', 'Value': 500000},
    {'Metric_Name': 'Forecast_Accuracy_Target', 'Value': 0.95},
    {'Metric_Name': 'Quarterly_Marketing_Budget', 'Value': 100000},
    {'Metric_Name': 'Target_CAC', 'Value': 50},
    {'Metric_Name': 'Target_ROI', 'Value': 3.0}
]

targets_df = pd.DataFrame(targets_data)

# Save to Excel file
with pd.ExcelWriter('sample_financial_data.xlsx', engine='openpyxl') as writer:
    transactions_df.to_excel(writer, sheet_name='Transactions', index=False)
    campaign_df.to_excel(writer, sheet_name='Campaign_Data', index=False)
    targets_df.to_excel(writer, sheet_name='Targets', index=False)

print("Sample Excel file 'sample_financial_data.xlsx' created successfully!")
print("\nFile contains:")
print(f"- Transactions: {len(transactions_df)} records")
print(f"- Campaign Data: {len(campaign_df)} records")
print(f"- Targets: {len(targets_df)} records")
print("\nThe recent Adwords campaigns are designed to trigger a CAC alert.")
