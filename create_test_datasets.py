#!/usr/bin/env python3
"""
Create 10 diverse Excel datasets to test the intelligent processing system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_dataset_1_saas_metrics():
    """Dataset 1: SaaS Metrics - Clean structure with MRR, CAC, Churn"""
    print("📊 Creating Dataset 1: SaaS Metrics")
    
    # Generate 12 months of SaaS data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    
    data = {
        'Month': dates,
        'MRR': np.random.uniform(50000, 150000, 12),
        'New_MRR': np.random.uniform(5000, 25000, 12),
        'Churn_Rate': np.random.uniform(0.02, 0.08, 12),
        'CAC': np.random.uniform(80, 200, 12),
        'LTV': np.random.uniform(2000, 8000, 12),
        'Active_Users': np.random.randint(1000, 5000, 12),
        'Revenue_Growth': np.random.uniform(0.05, 0.25, 12)
    }
    
    df = pd.DataFrame(data)
    df.to_excel('test_dataset_1_saas_metrics.xlsx', index=False)
    print(f"✅ Created: test_dataset_1_saas_metrics.xlsx ({len(df)} rows)")
    return "SaaS metrics with MRR, CAC, Churn Rate, LTV, Active Users, Revenue Growth"

def create_dataset_2_ecommerce_sales():
    """Dataset 2: E-commerce Sales - Product sales with categories"""
    print("📊 Creating Dataset 2: E-commerce Sales")
    
    products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Camera', 'Watch', 'Speaker', 'Keyboard']
    categories = ['Electronics', 'Accessories', 'Computing', 'Audio']
    
    data = []
    for i in range(100):
        product = np.random.choice(products)
        category = np.random.choice(categories)
        data.append({
            'Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(0, 365)],
            'Product': product,
            'Category': category,
            'Quantity': np.random.randint(1, 50),
            'Unit_Price': np.random.uniform(50, 2000),
            'Total_Sales': 0,  # Will calculate
            'Customer_ID': f"CUST_{np.random.randint(1000, 9999)}"
        })
    
    df = pd.DataFrame(data)
    df['Total_Sales'] = df['Quantity'] * df['Unit_Price']
    df.to_excel('test_dataset_2_ecommerce_sales.xlsx', index=False)
    print(f"✅ Created: test_dataset_2_ecommerce_sales.xlsx ({len(df)} rows)")
    return "E-commerce sales with products, categories, quantities, prices, and customer IDs"

def create_dataset_3_marketing_campaigns():
    """Dataset 3: Marketing Campaigns - Multi-channel campaigns"""
    print("📊 Creating Dataset 3: Marketing Campaigns")
    
    channels = ['Google Ads', 'Facebook', 'Instagram', 'LinkedIn', 'Email', 'Organic', 'Referral']
    campaign_types = ['Brand Awareness', 'Lead Generation', 'Sales Conversion', 'Retargeting']
    
    data = []
    for i in range(50):
        data.append({
            'Campaign_ID': f"CAMP_{i+1:03d}",
            'Campaign_Name': f"{np.random.choice(campaign_types)} {i+1}",
            'Channel': np.random.choice(channels),
            'Start_Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(0, 300)],
            'End_Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(300, 365)],
            'Budget': np.random.uniform(1000, 50000),
            'Spend': np.random.uniform(500, 45000),
            'Impressions': np.random.randint(10000, 1000000),
            'Clicks': np.random.randint(100, 10000),
            'Conversions': np.random.randint(5, 500),
            'Cost_Per_Conversion': 0  # Will calculate
        })
    
    df = pd.DataFrame(data)
    df['Cost_Per_Conversion'] = df['Spend'] / df['Conversions'].replace(0, 1)
    df.to_excel('test_dataset_3_marketing_campaigns.xlsx', index=False)
    print(f"✅ Created: test_dataset_3_marketing_campaigns.xlsx ({len(df)} rows)")
    return "Marketing campaigns with channels, budgets, spend, impressions, clicks, conversions"

def create_dataset_4_financial_transactions():
    """Dataset 4: Financial Transactions - Bank-like transaction data"""
    print("📊 Creating Dataset 4: Financial Transactions")
    
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Refund', 'Fee']
    categories = ['Salary', 'Rent', 'Utilities', 'Food', 'Transportation', 'Entertainment', 'Healthcare']
    
    data = []
    for i in range(200):
        trans_type = np.random.choice(transaction_types)
        amount = np.random.uniform(10, 5000)
        if trans_type in ['Withdrawal', 'Payment', 'Fee']:
            amount = -amount
        
        data.append({
            'Transaction_ID': f"TXN_{i+1:06d}",
            'Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(0, 365)],
            'Type': trans_type,
            'Category': np.random.choice(categories),
            'Amount': amount,
            'Balance': 0,  # Will calculate running balance
            'Description': f"{trans_type} - {np.random.choice(categories)}",
            'Account': f"ACC_{np.random.randint(1000, 9999)}"
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('Date')
    df['Balance'] = df['Amount'].cumsum() + 10000  # Starting balance
    df.to_excel('test_dataset_4_financial_transactions.xlsx', index=False)
    print(f"✅ Created: test_dataset_4_financial_transactions.xlsx ({len(df)} rows)")
    return "Financial transactions with types, categories, amounts, balances, and account info"

def create_dataset_5_inventory_management():
    """Dataset 5: Inventory Management - Product inventory levels"""
    print("📊 Creating Dataset 5: Inventory Management")
    
    products = ['Widget A', 'Widget B', 'Widget C', 'Gadget X', 'Gadget Y', 'Tool 1', 'Tool 2', 'Supply A']
    suppliers = ['Supplier Alpha', 'Supplier Beta', 'Supplier Gamma', 'Supplier Delta']
    
    data = []
    for i in range(80):
        data.append({
            'Product_ID': f"PROD_{i+1:04d}",
            'Product_Name': np.random.choice(products),
            'Supplier': np.random.choice(suppliers),
            'Current_Stock': np.random.randint(0, 1000),
            'Min_Stock_Level': np.random.randint(10, 100),
            'Max_Stock_Level': np.random.randint(200, 2000),
            'Unit_Cost': np.random.uniform(5, 500),
            'Selling_Price': np.random.uniform(10, 1000),
            'Last_Restock_Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(0, 365)],
            'Reorder_Quantity': np.random.randint(50, 500)
        })
    
    df = pd.DataFrame(data)
    df['Stock_Status'] = df.apply(lambda x: 'Low' if x['Current_Stock'] < x['Min_Stock_Level'] else 'OK', axis=1)
    df.to_excel('test_dataset_5_inventory_management.xlsx', index=False)
    print(f"✅ Created: test_dataset_5_inventory_management.xlsx ({len(df)} rows)")
    return "Inventory management with products, suppliers, stock levels, costs, and reorder info"

def create_dataset_6_hr_employee_data():
    """Dataset 6: HR Employee Data - Employee information and performance"""
    print("📊 Creating Dataset 6: HR Employee Data")
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    positions = ['Manager', 'Senior', 'Mid-level', 'Junior', 'Intern']
    locations = ['New York', 'San Francisco', 'London', 'Tokyo', 'Remote']
    
    data = []
    for i in range(60):
        hire_date = pd.date_range('2020-01-01', '2024-12-31')[np.random.randint(0, 1825)]
        data.append({
            'Employee_ID': f"EMP_{i+1:04d}",
            'Name': f"Employee {i+1}",
            'Department': np.random.choice(departments),
            'Position': np.random.choice(positions),
            'Location': np.random.choice(locations),
            'Hire_Date': hire_date,
            'Salary': np.random.uniform(40000, 150000),
            'Performance_Score': np.random.uniform(1, 5),
            'Years_Experience': np.random.randint(0, 15),
            'Manager_ID': f"MGR_{np.random.randint(1, 10):03d}"
        })
    
    df = pd.DataFrame(data)
    df['Tenure_Months'] = (datetime.now() - df['Hire_Date']).dt.days / 30
    df.to_excel('test_dataset_6_hr_employee_data.xlsx', index=False)
    print(f"✅ Created: test_dataset_6_hr_employee_data.xlsx ({len(df)} rows)")
    return "HR employee data with departments, positions, salaries, performance scores, and tenure"

def create_dataset_7_customer_feedback():
    """Dataset 7: Customer Feedback - Reviews and ratings"""
    print("📊 Creating Dataset 7: Customer Feedback")
    
    products = ['Product A', 'Product B', 'Product C', 'Service X', 'Service Y']
    categories = ['Excellent', 'Good', 'Average', 'Poor', 'Terrible']
    
    data = []
    for i in range(150):
        rating = np.random.randint(1, 6)
        data.append({
            'Review_ID': f"REV_{i+1:05d}",
            'Customer_ID': f"CUST_{np.random.randint(1000, 9999)}",
            'Product': np.random.choice(products),
            'Rating': rating,
            'Review_Text': f"This is a {'great' if rating >= 4 else 'poor'} product with {'excellent' if rating >= 4 else 'subpar'} quality.",
            'Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(0, 365)],
            'Helpful_Votes': np.random.randint(0, 50),
            'Verified_Purchase': np.random.choice([True, False])
        })
    
    df = pd.DataFrame(data)
    df['Sentiment'] = df['Rating'].apply(lambda x: 'Positive' if x >= 4 else 'Negative' if x <= 2 else 'Neutral')
    df.to_excel('test_dataset_7_customer_feedback.xlsx', index=False)
    print(f"✅ Created: test_dataset_7_customer_feedback.xlsx ({len(df)} rows)")
    return "Customer feedback with ratings, reviews, sentiment analysis, and helpful votes"

def create_dataset_8_sales_pipeline():
    """Dataset 8: Sales Pipeline - CRM-style opportunity tracking"""
    print("📊 Creating Dataset 8: Sales Pipeline")
    
    stages = ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    sources = ['Website', 'Referral', 'Cold Call', 'Trade Show', 'Social Media', 'Email Campaign']
    
    data = []
    for i in range(75):
        stage = np.random.choice(stages)
        data.append({
            'Opportunity_ID': f"OPP_{i+1:04d}",
            'Company_Name': f"Company {i+1}",
            'Contact_Name': f"Contact {i+1}",
            'Stage': stage,
            'Source': np.random.choice(sources),
            'Deal_Value': np.random.uniform(1000, 100000),
            'Probability': np.random.uniform(0.1, 1.0),
            'Expected_Close_Date': pd.date_range('2024-01-01', '2025-12-31')[np.random.randint(0, 730)],
            'Created_Date': pd.date_range('2024-01-01', '2024-12-31')[np.random.randint(0, 365)],
            'Sales_Rep': f"Rep_{np.random.randint(1, 10):02d}"
        })
    
    df = pd.DataFrame(data)
    df['Weighted_Value'] = df['Deal_Value'] * df['Probability']
    df.to_excel('test_dataset_8_sales_pipeline.xlsx', index=False)
    print(f"✅ Created: test_dataset_8_sales_pipeline.xlsx ({len(df)} rows)")
    return "Sales pipeline with opportunities, stages, deal values, probabilities, and close dates"

def create_dataset_9_website_analytics():
    """Dataset 9: Website Analytics - Traffic and engagement metrics"""
    print("📊 Creating Dataset 9: Website Analytics")
    
    pages = ['Home', 'Products', 'About', 'Contact', 'Blog', 'Pricing', 'Support']
    traffic_sources = ['Organic', 'Paid', 'Direct', 'Referral', 'Social', 'Email']
    
    data = []
    for i in range(30):  # 30 days of data
        date = pd.date_range('2024-01-01', '2024-12-31')[i]
        for page in pages:
            data.append({
                'Date': date,
                'Page': page,
                'Page_Views': np.random.randint(100, 10000),
                'Unique_Visitors': np.random.randint(50, 5000),
                'Bounce_Rate': np.random.uniform(0.2, 0.8),
                'Avg_Session_Duration': np.random.uniform(30, 300),
                'Traffic_Source': np.random.choice(traffic_sources),
                'Conversions': np.random.randint(0, 100)
            })
    
    df = pd.DataFrame(data)
    df['Conversion_Rate'] = df['Conversions'] / df['Page_Views']
    df.to_excel('test_dataset_9_website_analytics.xlsx', index=False)
    print(f"✅ Created: test_dataset_9_website_analytics.xlsx ({len(df)} rows)")
    return "Website analytics with page views, visitors, bounce rates, session duration, and conversions"

def create_dataset_10_budget_planning():
    """Dataset 10: Budget Planning - Department budgets and actuals"""
    print("📊 Creating Dataset 10: Budget Planning")
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'R&D']
    categories = ['Personnel', 'Equipment', 'Software', 'Travel', 'Training', 'Office Supplies', 'Utilities']
    
    data = []
    for dept in departments:
        for category in categories:
            budget = np.random.uniform(10000, 200000)
            actual = budget * np.random.uniform(0.8, 1.2)
            data.append({
                'Department': dept,
                'Category': category,
                'Budget_Amount': budget,
                'Actual_Amount': actual,
                'Variance': actual - budget,
                'Variance_Percentage': ((actual - budget) / budget) * 100,
                'Quarter': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4']),
                'Year': 2024,
                'Status': 'Over Budget' if actual > budget else 'Under Budget'
            })
    
    df = pd.DataFrame(data)
    df.to_excel('test_dataset_10_budget_planning.xlsx', index=False)
    print(f"✅ Created: test_dataset_10_budget_planning.xlsx ({len(df)} rows)")
    return "Budget planning with departments, categories, budget vs actual amounts, and variance analysis"

def create_all_datasets():
    """Create all 10 test datasets"""
    print("🚀 Creating 10 Diverse Excel Test Datasets")
    print("=" * 60)
    
    datasets = []
    
    # Create all datasets
    datasets.append(create_dataset_1_saas_metrics())
    datasets.append(create_dataset_2_ecommerce_sales())
    datasets.append(create_dataset_3_marketing_campaigns())
    datasets.append(create_dataset_4_financial_transactions())
    datasets.append(create_dataset_5_inventory_management())
    datasets.append(create_dataset_6_hr_employee_data())
    datasets.append(create_dataset_7_customer_feedback())
    datasets.append(create_dataset_8_sales_pipeline())
    datasets.append(create_dataset_9_website_analytics())
    datasets.append(create_dataset_10_budget_planning())
    
    print("\n🎉 ALL DATASETS CREATED SUCCESSFULLY!")
    print("=" * 60)
    
    # Create summary
    summary_data = []
    for i, description in enumerate(datasets, 1):
        filename = f"test_dataset_{i}_{['saas_metrics', 'ecommerce_sales', 'marketing_campaigns', 'financial_transactions', 'inventory_management', 'hr_employee_data', 'customer_feedback', 'sales_pipeline', 'website_analytics', 'budget_planning'][i-1]}.xlsx"
        summary_data.append({
            'Dataset': i,
            'Filename': filename,
            'Description': description,
            'Expected_Output': 'Intelligent processing will extract financial metrics, create KPIs, and generate CEO/CFO insights'
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel('test_datasets_summary.xlsx', index=False)
    
    print("📋 DATASET SUMMARY:")
    for i, row in summary_df.iterrows():
        print(f"   {row['Dataset']}. {row['Filename']}")
        print(f"      📊 {row['Description']}")
        print(f"      🎯 {row['Expected_Output']}")
        print()
    
    print("🌟 TESTING INSTRUCTIONS:")
    print("=" * 60)
    print("1. Upload each Excel file to your Aura platform")
    print("2. Observe how the intelligent processor handles different structures")
    print("3. Check the Dashboard for extracted KPIs")
    print("4. Test CEO/CFO analysis with different data types")
    print("5. Verify that all files are processed without errors")
    print("\n🚀 Your intelligent Excel processing system is ready for comprehensive testing!")

if __name__ == "__main__":
    create_all_datasets()
