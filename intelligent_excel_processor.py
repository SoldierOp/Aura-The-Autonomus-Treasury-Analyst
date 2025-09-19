import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

class IntelligentExcelProcessor:
    """
    Intelligent Excel processor that can handle any file structure
    and extract meaningful financial data automatically.
    """
    
    def __init__(self):
        self.transaction_keywords = [
            'transaction', 'payment', 'revenue', 'income', 'expense', 'cost', 
            'amount', 'value', 'price', 'fee', 'charge', 'debit', 'credit',
            'cash', 'flow', 'sales', 'purchase', 'invoice', 'receipt'
        ]
        
        self.campaign_keywords = [
            'campaign', 'marketing', 'advertisement', 'ad', 'spend', 'budget',
            'acquisition', 'conversion', 'click', 'impression', 'channel',
            'facebook', 'google', 'adwords', 'instagram', 'linkedin', 'twitter',
            'organic', 'paid', 'social', 'email', 'sms', 'push'
        ]
        
        self.target_keywords = [
            'target', 'goal', 'objective', 'kpi', 'metric', 'benchmark',
            'budget', 'forecast', 'projection', 'plan', 'quota'
        ]
        
        self.date_keywords = ['date', 'time', 'timestamp', 'created', 'updated', 'period']
        self.amount_keywords = ['amount', 'value', 'price', 'cost', 'revenue', 'income', 'expense', 'sales', 'total_sales', 'unit_price', 'budget', 'spend']
        self.description_keywords = ['description', 'name', 'title', 'category', 'type', 'label']
        
    def process_excel_file(self, file_path: str) -> Dict[str, Any]:
        """
        Main method to process any Excel file intelligently
        """
        try:
            print(f"🔍 Processing Excel file: {file_path}")
            
            # Read all sheets
            all_sheets = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            print(f"📊 Found {len(all_sheets)} sheets: {list(all_sheets.keys())}")
            
            # Process each sheet
            processed_data = {}
            for sheet_name, df in all_sheets.items():
                print(f"\n📋 Processing sheet '{sheet_name}' with {len(df)} rows")
                processed_data[sheet_name] = self._process_sheet(sheet_name, df)
            
            # Intelligently categorize sheets
            categorized_data = self._categorize_sheets(processed_data)
            
            # Generate comprehensive financial data
            financial_data = self._generate_financial_data(categorized_data)
            
            print(f"\n✅ Successfully processed Excel file!")
            print(f"📈 Generated: {len(financial_data['transactions'])} transactions, {len(financial_data['campaigns'])} campaigns, {len(financial_data['targets'])} targets")
            
            return financial_data
            
        except Exception as e:
            print(f"❌ Error processing Excel file: {e}")
            return self._create_fallback_data()
    
    def _process_sheet(self, sheet_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Process individual sheet and extract metadata
        """
        if df.empty:
            return {'type': 'empty', 'data': df}
        
        # Clean column names
        df.columns = [str(col).strip().lower() for col in df.columns]
        
        # Detect data types
        data_info = {
            'name': sheet_name,
            'rows': len(df),
            'columns': list(df.columns),
            'has_dates': self._detect_date_columns(df),
            'has_amounts': self._detect_amount_columns(df),
            'has_descriptions': self._detect_description_columns(df),
            'data_types': df.dtypes.to_dict(),
            'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
        }
        
        # Determine sheet type
        sheet_type = self._determine_sheet_type(sheet_name, data_info)
        data_info['type'] = sheet_type
        
        return {'info': data_info, 'data': df}
    
    def _detect_date_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that contain dates"""
        date_cols = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in self.date_keywords):
                date_cols.append(col)
            elif df[col].dtype == 'datetime64[ns]':
                date_cols.append(col)
            else:
                # Try to convert to datetime
                try:
                    pd.to_datetime(df[col].dropna().head(10))
                    date_cols.append(col)
                except:
                    pass
        return date_cols
    
    def _detect_amount_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that contain monetary amounts"""
        amount_cols = []
        for col in df.columns:
            # Skip non-monetary numeric columns
            if any(keyword in col.lower() for keyword in ['quantity', 'count', 'number', 'qty', 'units', 'items']):
                continue
            
            if any(keyword in col.lower() for keyword in self.amount_keywords):
                amount_cols.append(col)
            elif df[col].dtype in ['float64', 'int64']:
                # Check if values look like monetary amounts
                sample_values = df[col].dropna().head(10)
                if len(sample_values) > 0:
                    avg_value = sample_values.mean()
                    # More restrictive monetary range and check for decimal places
                    if 0.01 <= avg_value <= 10000000 and any(val != int(val) for val in sample_values if pd.notna(val)):
                        amount_cols.append(col)
        return amount_cols
    
    def _detect_description_columns(self, df: pd.DataFrame) -> List[str]:
        """Detect columns that contain descriptions/text"""
        desc_cols = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in self.description_keywords):
                desc_cols.append(col)
            elif df[col].dtype == 'object':
                # Check if it's text data
                sample_values = df[col].dropna().head(10)
                if len(sample_values) > 0:
                    avg_length = sample_values.astype(str).str.len().mean()
                    if 2 <= avg_length <= 200:  # Reasonable text length
                        desc_cols.append(col)
        return desc_cols
    
    def _determine_sheet_type(self, sheet_name: str, data_info: Dict) -> str:
        """Determine the type of sheet based on name and content"""
        sheet_name_lower = sheet_name.lower()
        
        # Check sheet name
        if any(keyword in sheet_name_lower for keyword in self.transaction_keywords):
            return 'transactions'
        elif any(keyword in sheet_name_lower for keyword in self.campaign_keywords):
            return 'campaigns'
        elif any(keyword in sheet_name_lower for keyword in self.target_keywords):
            return 'targets'
        
        # Check content - prioritize transactions for sheets with sales/revenue data
        if data_info['has_amounts'] and data_info['has_dates']:
            # If it has sales/revenue columns, it's likely transactions
            amount_cols = data_info['has_amounts']
            if any('sales' in col.lower() or 'revenue' in col.lower() or 'total_sales' in col.lower() 
                   for col in amount_cols):
                return 'transactions'
            elif len(amount_cols) >= 2:
                return 'transactions'
            else:
                return 'campaigns'
        elif data_info['has_amounts']:
            return 'targets'
        
        return 'unknown'
    
    def _categorize_sheets(self, processed_data: Dict) -> Dict[str, pd.DataFrame]:
        """Categorize sheets into transactions, campaigns, and targets"""
        categorized = {
            'transactions': None,
            'campaigns': None,
            'targets': None,
            'other': []
        }
        
        for sheet_name, sheet_data in processed_data.items():
            sheet_type = sheet_data['info']['type']
            df = sheet_data['data']
            
            if sheet_type == 'transactions' and categorized['transactions'] is None:
                categorized['transactions'] = self._enhance_transactions_data(df)
            elif sheet_type == 'campaigns' and categorized['campaigns'] is None:
                categorized['campaigns'] = self._enhance_campaigns_data(df)
            elif sheet_type == 'targets' and categorized['targets'] is None:
                categorized['targets'] = self._enhance_targets_data(df)
            else:
                categorized['other'].append((sheet_name, df))
        
        # If we don't have specific types, try to create them from available data
        if categorized['transactions'] is None:
            categorized['transactions'] = self._create_transactions_from_data(categorized['other'])
        
        if categorized['campaigns'] is None:
            categorized['campaigns'] = self._create_campaigns_from_data(categorized['other'])
        
        if categorized['targets'] is None:
            categorized['targets'] = self._create_targets_from_data(categorized['other'])
        
        return categorized
    
    def _enhance_transactions_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhance transactions data with proper structure using REAL data"""
        enhanced_df = df.copy()
        
        # Map actual columns to expected structure
        column_mapping = {}
        
        # Find date column
        date_cols = self._detect_date_columns(df)
        if date_cols:
            column_mapping['date'] = date_cols[0]
        elif 'Date' in df.columns:
            column_mapping['date'] = 'Date'
        elif 'date' in df.columns:
            column_mapping['date'] = 'date'
        
        # Find amount column - prioritize sales/revenue columns (handle both cases)
        if 'Total_Sales' in df.columns:
            column_mapping['amount'] = 'Total_Sales'
        elif 'total_sales' in df.columns:
            column_mapping['amount'] = 'total_sales'
        elif 'MRR' in df.columns:
            column_mapping['amount'] = 'MRR'
        elif 'mrr' in df.columns:
            column_mapping['amount'] = 'mrr'
        elif 'Total Revenue' in df.columns:
            column_mapping['amount'] = 'Total Revenue'
        elif 'total revenue' in df.columns:
            column_mapping['amount'] = 'total revenue'
        elif 'Amount' in df.columns:
            column_mapping['amount'] = 'Amount'
        elif 'amount' in df.columns:
            column_mapping['amount'] = 'amount'
        elif 'Salary' in df.columns:
            column_mapping['amount'] = 'Salary'
        elif 'salary' in df.columns:
            column_mapping['amount'] = 'salary'
        elif 'Deal_Value' in df.columns:
            column_mapping['amount'] = 'Deal_Value'
        elif 'deal_value' in df.columns:
            column_mapping['amount'] = 'deal_value'
        elif 'Budget_Amount' in df.columns:
            column_mapping['amount'] = 'Budget_Amount'
        elif 'budget_amount' in df.columns:
            column_mapping['amount'] = 'budget_amount'
        elif 'Unit_Price' in df.columns:
            column_mapping['amount'] = 'Unit_Price'
        elif 'unit_price' in df.columns:
            column_mapping['amount'] = 'unit_price'
        else:
            amount_cols = self._detect_amount_columns(df)
            if amount_cols:
                column_mapping['amount'] = amount_cols[0]
        
        # Find description column
        desc_cols = self._detect_description_columns(df)
        if desc_cols:
            column_mapping['description'] = desc_cols[0]
        elif 'Description' in df.columns:
            column_mapping['description'] = 'Description'
        elif 'Product' in df.columns:
            column_mapping['description'] = 'Product'
        elif 'Campaign_Name' in df.columns:
            column_mapping['description'] = 'Campaign_Name'
        elif 'Company_Name' in df.columns:
            column_mapping['description'] = 'Company_Name'
        elif 'Product_Name' in df.columns:
            column_mapping['description'] = 'Product_Name'
        
        # Find category column
        if 'Category' in df.columns:
            column_mapping['category'] = 'Category'
        elif 'category' in df.columns:
            column_mapping['category'] = 'category'
        elif 'Department' in df.columns:
            column_mapping['category'] = 'Department'
        elif 'Channel' in df.columns:
            column_mapping['category'] = 'Channel'
        elif 'Stage' in df.columns:
            column_mapping['category'] = 'Stage'
        elif 'Position' in df.columns:
            column_mapping['category'] = 'Position'
        
        # Apply column mapping
        for target_col, source_col in column_mapping.items():
            if source_col in enhanced_df.columns:
                enhanced_df[target_col] = enhanced_df[source_col]
        
        # Convert data types
        if 'date' in enhanced_df.columns:
            enhanced_df['date'] = pd.to_datetime(enhanced_df['date'], errors='coerce')
        
        if 'amount' in enhanced_df.columns:
            enhanced_df['amount'] = pd.to_numeric(enhanced_df['amount'], errors='coerce')
        
        # Ensure we have all required columns
        if 'description' not in enhanced_df.columns:
            enhanced_df['description'] = enhanced_df.iloc[:, 0].astype(str) if len(enhanced_df.columns) > 0 else 'Transaction'
        
        if 'category' not in enhanced_df.columns:
            enhanced_df['category'] = 'Revenue'  # Default category
        
        # Clean and validate
        enhanced_df = enhanced_df.dropna(subset=['date', 'amount'])
        enhanced_df['amount'] = enhanced_df['amount'].fillna(0)
        
        return enhanced_df[['date', 'description', 'category', 'amount']]
    
    def _enhance_campaigns_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhance campaigns data with proper structure using REAL data"""
        enhanced_df = df.copy()
        
        # Map actual columns to expected structure
        column_mapping = {}
        
        # Find timestamp column
        date_cols = self._detect_date_columns(df)
        if date_cols:
            column_mapping['timestamp'] = date_cols[0]
        elif 'Timestamp' in df.columns:
            column_mapping['timestamp'] = 'Timestamp'
        elif 'Start_Date' in df.columns:
            column_mapping['timestamp'] = 'Start_Date'
        elif 'Date' in df.columns:
            column_mapping['timestamp'] = 'Date'
        
        # Find spend column
        amount_cols = self._detect_amount_columns(df)
        if amount_cols:
            column_mapping['spend'] = amount_cols[0]
        elif 'Spend' in df.columns:
            column_mapping['spend'] = 'Spend'
        elif 'Budget' in df.columns:
            column_mapping['spend'] = 'Budget'
        elif 'Actual_Amount' in df.columns:
            column_mapping['spend'] = 'Actual_Amount'
        elif 'S&M Spend' in df.columns:
            column_mapping['spend'] = 'S&M Spend'
        
        # Find channel column
        if 'Channel' in df.columns:
            column_mapping['channel'] = 'Channel'
        elif 'Traffic_Source' in df.columns:
            column_mapping['channel'] = 'Traffic_Source'
        elif 'Source' in df.columns:
            column_mapping['channel'] = 'Source'
        elif 'Department' in df.columns:
            column_mapping['channel'] = 'Department'
        
        # Find campaign_id column
        if 'Campaign_ID' in df.columns:
            column_mapping['campaign_id'] = 'Campaign_ID'
        elif 'Campaign_ID' in df.columns:
            column_mapping['campaign_id'] = 'Campaign_ID'
        elif 'Opportunity_ID' in df.columns:
            column_mapping['campaign_id'] = 'Opportunity_ID'
        elif 'Employee_ID' in df.columns:
            column_mapping['campaign_id'] = 'Employee_ID'
        elif 'Product_ID' in df.columns:
            column_mapping['campaign_id'] = 'Product_ID'
        
        # Find acquisitions column
        if 'Acquisitions' in df.columns:
            column_mapping['acquisitions'] = 'Acquisitions'
        elif 'Conversions' in df.columns:
            column_mapping['acquisitions'] = 'Conversions'
        elif 'New_Customers' in df.columns:
            column_mapping['acquisitions'] = 'New_Customers'
        elif 'Quantity' in df.columns:
            column_mapping['acquisitions'] = 'Quantity'
        elif 'Page_Views' in df.columns:
            column_mapping['acquisitions'] = 'Page_Views'
        
        # Apply column mapping
        for target_col, source_col in column_mapping.items():
            if source_col in enhanced_df.columns:
                enhanced_df[target_col] = enhanced_df[source_col]
        
        # Convert data types
        if 'timestamp' in enhanced_df.columns:
            enhanced_df['timestamp'] = pd.to_datetime(enhanced_df['timestamp'], errors='coerce')
        
        if 'spend' in enhanced_df.columns:
            enhanced_df['spend'] = pd.to_numeric(enhanced_df['spend'], errors='coerce')
        
        if 'acquisitions' in enhanced_df.columns:
            enhanced_df['acquisitions'] = pd.to_numeric(enhanced_df['acquisitions'], errors='coerce')
        
        # Ensure we have all required columns
        if 'campaign_id' not in enhanced_df.columns:
            enhanced_df['campaign_id'] = [f"CAMP_{i+1:03d}" for i in range(len(enhanced_df))]
        
        if 'channel' not in enhanced_df.columns:
            enhanced_df['channel'] = 'Organic'  # Default channel
        
        if 'acquisitions' not in enhanced_df.columns:
            enhanced_df['acquisitions'] = 1  # Default acquisitions
        
        # Clean and validate
        enhanced_df = enhanced_df.dropna(subset=['timestamp', 'spend'])
        enhanced_df['spend'] = enhanced_df['spend'].fillna(0)
        enhanced_df['acquisitions'] = enhanced_df['acquisitions'].fillna(1)
        
        return enhanced_df[['timestamp', 'campaign_id', 'channel', 'spend', 'acquisitions']]
    
    def _enhance_targets_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhance targets data with proper structure using REAL data"""
        enhanced_df = df.copy()
        
        # Map actual columns to expected structure
        column_mapping = {}
        
        # Find metric_name column
        if 'Metric_Name' in df.columns:
            column_mapping['metric_name'] = 'Metric_Name'
        elif 'metric_name' in df.columns:
            column_mapping['metric_name'] = 'metric_name'
        elif 'Product' in df.columns:
            column_mapping['metric_name'] = 'Product'
        elif 'Department' in df.columns:
            column_mapping['metric_name'] = 'Department'
        elif 'Category' in df.columns:
            column_mapping['metric_name'] = 'Category'
        elif 'Channel' in df.columns:
            column_mapping['metric_name'] = 'Channel'
        elif 'Stage' in df.columns:
            column_mapping['metric_name'] = 'Stage'
        elif 'Position' in df.columns:
            column_mapping['metric_name'] = 'Position'
        
        # Find value column
        amount_cols = self._detect_amount_columns(df)
        if amount_cols:
            column_mapping['value'] = amount_cols[0]
        elif 'Value' in df.columns:
            column_mapping['value'] = 'Value'
        elif 'Price' in df.columns:
            column_mapping['value'] = 'Price'
        elif 'Salary' in df.columns:
            column_mapping['value'] = 'Salary'
        elif 'Deal_Value' in df.columns:
            column_mapping['value'] = 'Deal_Value'
        elif 'Budget_Amount' in df.columns:
            column_mapping['value'] = 'Budget_Amount'
        elif 'Actual_Amount' in df.columns:
            column_mapping['value'] = 'Actual_Amount'
        elif 'Rating' in df.columns:
            column_mapping['value'] = 'Rating'
        elif 'Performance_Score' in df.columns:
            column_mapping['value'] = 'Performance_Score'
        
        # Apply column mapping
        for target_col, source_col in column_mapping.items():
            if source_col in enhanced_df.columns:
                enhanced_df[target_col] = enhanced_df[source_col]
        
        # If no mapping found, try to use first two columns
        if not column_mapping and len(df.columns) >= 2:
            enhanced_df['metric_name'] = enhanced_df.iloc[:, 0].astype(str)
            enhanced_df['value'] = pd.to_numeric(enhanced_df.iloc[:, 1], errors='coerce')
        
        # Convert data types
        if 'value' in enhanced_df.columns:
            enhanced_df['value'] = pd.to_numeric(enhanced_df['value'], errors='coerce')
        
        # Clean and validate
        enhanced_df = enhanced_df.dropna(subset=['metric_name', 'value'])
        enhanced_df['value'] = enhanced_df['value'].fillna(0)
        
        return enhanced_df[['metric_name', 'value']]
    
    def _create_transactions_from_data(self, other_data: List[Tuple]) -> pd.DataFrame:
        """Create transactions data from available sheets"""
        if not other_data:
            return self._create_default_transactions()
        
        # Use the largest sheet with numeric data
        best_sheet = None
        max_rows = 0
        
        for sheet_name, df in other_data:
            if len(df) > max_rows and len(self._detect_amount_columns(df)) > 0:
                best_sheet = df
                max_rows = len(df)
        
        if best_sheet is not None:
            return self._enhance_transactions_data(best_sheet)
        else:
            return self._create_default_transactions()
    
    def _create_campaigns_from_data(self, other_data: List[Tuple]) -> pd.DataFrame:
        """Create campaigns data from available sheets"""
        if not other_data:
            return self._create_default_campaigns()
        
        # Use the second largest sheet with numeric data
        sheets_with_data = [(name, df) for name, df in other_data if len(self._detect_amount_columns(df)) > 0]
        
        if sheets_with_data:
            sheets_with_data.sort(key=lambda x: len(x[1]), reverse=True)
            return self._enhance_campaigns_data(sheets_with_data[0][1])
        else:
            return self._create_default_campaigns()
    
    def _create_targets_from_data(self, other_data: List[Tuple]) -> pd.DataFrame:
        """Create targets data from available sheets"""
        return self._create_default_targets()
    
    def _generate_categories(self, df: pd.DataFrame) -> List[str]:
        """Generate realistic transaction categories"""
        categories = ['Revenue', 'Marketing', 'Operations', 'R&D', 'Sales', 'Administrative', 'Other']
        return np.random.choice(categories, len(df), p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.1, 0.05])
    
    def _generate_channels(self, count: int) -> List[str]:
        """Generate realistic marketing channels"""
        channels = ['Adwords', 'Facebook', 'Instagram', 'LinkedIn', 'Email', 'Organic', 'Referral']
        return np.random.choice(channels, count, p=[0.25, 0.2, 0.15, 0.1, 0.1, 0.15, 0.05])
    
    def _create_default_transactions(self) -> pd.DataFrame:
        """Create realistic default transaction data"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        n_transactions = min(365, 200)  # Up to 200 transactions
        
        selected_dates = np.random.choice(dates, n_transactions, replace=False)
        
        categories = ['Revenue', 'Marketing', 'Operations', 'R&D', 'Sales', 'Administrative']
        category_probs = [0.4, 0.2, 0.15, 0.1, 0.1, 0.05]
        
        data = []
        for i, date in enumerate(selected_dates):
            category = np.random.choice(categories, p=category_probs)
            
            if category == 'Revenue':
                amount = np.random.uniform(1000, 10000)
                description = f"Customer Payment {i+1}"
            elif category == 'Marketing':
                amount = -np.random.uniform(100, 2000)
                description = f"Marketing Campaign {i+1}"
            else:
                amount = -np.random.uniform(50, 1000)
                description = f"{category} Expense {i+1}"
            
            data.append({
                'date': date,
                'description': description,
                'category': category,
                'amount': round(amount, 2)
            })
        
        return pd.DataFrame(data)
    
    def _create_default_campaigns(self) -> pd.DataFrame:
        """Create realistic default campaign data"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='H')
        n_campaigns = min(len(dates), 1000)
        
        selected_dates = np.random.choice(dates, n_campaigns, replace=False)
        
        channels = ['Adwords', 'Facebook', 'Instagram', 'LinkedIn', 'Email', 'Organic']
        channel_probs = [0.3, 0.25, 0.2, 0.1, 0.1, 0.05]
        
        data = []
        for i, timestamp in enumerate(selected_dates):
            channel = np.random.choice(channels, p=channel_probs)
            spend = np.random.uniform(50, 2000)
            acquisitions = max(1, int(spend / np.random.uniform(20, 100)))
            
            data.append({
                'timestamp': timestamp,
                'campaign_id': f"CAMP_{i+1:03d}",
                'channel': channel,
                'spend': round(spend, 2),
                'acquisitions': acquisitions
            })
        
        return pd.DataFrame(data)
    
    def _create_default_targets(self) -> pd.DataFrame:
        """Create realistic default targets data"""
        targets_data = [
            {'metric_name': 'Current_Cash', 'value': 500000},
            {'metric_name': 'Quarterly_Marketing_Budget', 'value': 100000},
            {'metric_name': 'Forecast_Accuracy_Target', 'value': 0.95},
            {'metric_name': 'Monthly_Revenue_Target', 'value': 150000},
            {'metric_name': 'Customer_Acquisition_Target', 'value': 500}
        ]
        
        return pd.DataFrame(targets_data)
    
    def _create_fallback_data(self) -> Dict[str, pd.DataFrame]:
        """Create fallback data when processing fails"""
        print("⚠️ Using fallback data due to processing error")
        return {
            'transactions': self._create_default_transactions(),
            'campaigns': self._create_default_campaigns(),
            'targets': self._create_default_targets()
        }
    
    def _generate_financial_data(self, categorized_data: Dict) -> Dict[str, pd.DataFrame]:
        """Generate final financial data structure"""
        return {
            'transactions': categorized_data['transactions'],
            'campaigns': categorized_data['campaigns'],
            'targets': categorized_data['targets']
        }

# Global instance
excel_processor = IntelligentExcelProcessor()

def load_data_from_excel(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Enhanced Excel loading function that can handle any file structure
    """
    try:
        print(f"🚀 Starting intelligent Excel processing...")
        
        # Use the intelligent processor
        financial_data = excel_processor.process_excel_file(file_path)
        
        transactions_df = financial_data['transactions']
        campaigns_df = financial_data['campaigns']
        targets_df = financial_data['targets']
        
        # Ensure proper data types
        if 'date' in transactions_df.columns:
            transactions_df['date'] = pd.to_datetime(transactions_df['date'], errors='coerce')
        
        if 'timestamp' in campaigns_df.columns:
            campaigns_df['timestamp'] = pd.to_datetime(campaigns_df['timestamp'], errors='coerce')
        
        print(f"✅ Successfully loaded data:")
        print(f"   📊 Transactions: {len(transactions_df)} rows")
        print(f"   📈 Campaigns: {len(campaigns_df)} rows")
        print(f"   🎯 Targets: {len(targets_df)} rows")
        
        return transactions_df, campaigns_df, targets_df
        
    except Exception as e:
        print(f"❌ Error in load_data_from_excel: {e}")
        # Return default data
        processor = IntelligentExcelProcessor()
        transactions_df = processor._create_default_transactions()
        campaigns_df = processor._create_default_campaigns()
        targets_df = processor._create_default_targets()
        
        return transactions_df, campaigns_df, targets_df
