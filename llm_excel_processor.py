#!/usr/bin/env python3
"""
LLM-Powered Excel Processor using Gemini API
Intelligently interprets any Excel structure without predefined mappings
"""

import pandas as pd
import requests
import json
from typing import Dict, List, Tuple, Any
import os
from config import GEMINI_API_KEY, GEMINI_API_URL

class LLMExcelProcessor:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
    
    def analyze_excel_structure(self, file_path: str) -> Dict[str, Any]:
        """
        Use Gemini API to analyze Excel file structure and determine column mappings
        """
        try:
            # Read all sheets
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            # Prepare data for LLM analysis
            analysis_data = {}
            for sheet_name, df in excel_data.items():
                # Sample first 5 rows and column info
                sample_data = df.head(5).to_dict('records')
                analysis_data[sheet_name] = {
                    'columns': list(df.columns),
                    'sample_data': sample_data,
                    'row_count': len(df)
                }
            
            # Create prompt for Gemini
            prompt = f"""
            Analyze this Excel file structure and determine the column mappings for financial analysis.
            
            Excel Data:
            {json.dumps(analysis_data, indent=2, default=str)}
            
            Please identify:
            1. Which sheet contains TRANSACTIONS (financial transactions with dates, amounts, descriptions)
            2. Which sheet contains CAMPAIGN DATA (marketing campaigns with spend, acquisitions, channels)
            3. Which sheet contains TARGETS (KPIs, goals, metrics)
            
            For each sheet, identify:
            - Date column (for time-based analysis)
            - Amount/Money column (for financial calculations)
            - Description/Name column (for transaction descriptions)
            - Category/Type column (for categorization)
            - Channel/Source column (for campaign data)
            - Spend/Cost column (for campaign costs)
            - Acquisitions/Conversions column (for campaign results)
            - Metric name column (for targets)
            - Value column (for target values)
            
            Return your analysis in this JSON format:
            {{
                "transactions_sheet": "sheet_name",
                "campaigns_sheet": "sheet_name", 
                "targets_sheet": "sheet_name",
                "column_mappings": {{
                    "transactions": {{
                        "date": "column_name",
                        "amount": "column_name",
                        "description": "column_name",
                        "category": "column_name"
                    }},
                    "campaigns": {{
                        "date": "column_name",
                        "spend": "column_name",
                        "channel": "column_name",
                        "acquisitions": "column_name"
                    }},
                    "targets": {{
                        "metric_name": "column_name",
                        "value": "column_name"
                    }}
                }}
            }}
            
            If a column doesn't exist, use null. Be intelligent about column names - they might be in different languages or formats.
            """
            
            # Call Gemini API
            response = self.call_gemini_api(prompt)
            
            # Parse response
            try:
                # Clean response - remove markdown formatting if present
                clean_response = response.strip()
                if clean_response.startswith('```json'):
                    clean_response = clean_response[7:]
                if clean_response.endswith('```'):
                    clean_response = clean_response[:-3]
                clean_response = clean_response.strip()
                
                analysis = json.loads(clean_response)
                print(f"✅ LLM successfully analyzed Excel structure")
                return analysis
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Raw response: {response}")
                # Fallback to basic analysis
                return self.fallback_analysis(excel_data)
                
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return self.fallback_analysis(excel_data)
    
    def call_gemini_api(self, prompt: str) -> str:
        """
        Call Gemini API with the analysis prompt
        """
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 1,
                    "topP": 0.8,
                    "maxOutputTokens": 2048,
                }
            }
            
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code == 429:
                print("⚠️ Gemini API quota exceeded, using fallback analysis")
                return ""
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return ""
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return ""
    
    def fallback_analysis(self, excel_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Fallback analysis when LLM fails
        """
        print("Using fallback analysis...")
        
        # Simple heuristic-based analysis
        analysis = {
            "transactions_sheet": None,
            "campaigns_sheet": None,
            "targets_sheet": None,
            "column_mappings": {
                "transactions": {},
                "campaigns": {},
                "targets": {}
            }
        }
        
        for sheet_name, df in excel_data.items():
            columns = [col.lower() for col in df.columns]
            
            # Check for transactions
            if any(keyword in ' '.join(columns) for keyword in ['amount', 'transaction', 'payment', 'revenue']):
                analysis["transactions_sheet"] = sheet_name
                # Map columns
                for col in df.columns:
                    col_lower = col.lower()
                    if 'date' in col_lower:
                        analysis["column_mappings"]["transactions"]["date"] = col
                    elif 'amount' in col_lower or 'value' in col_lower:
                        analysis["column_mappings"]["transactions"]["amount"] = col
                    elif 'description' in col_lower or 'name' in col_lower:
                        analysis["column_mappings"]["transactions"]["description"] = col
                    elif 'category' in col_lower or 'type' in col_lower:
                        analysis["column_mappings"]["transactions"]["category"] = col
            
            # Check for campaigns
            elif any(keyword in ' '.join(columns) for keyword in ['campaign', 'spend', 'channel', 'acquisition']):
                analysis["campaigns_sheet"] = sheet_name
                # Map columns
                for col in df.columns:
                    col_lower = col.lower()
                    if 'date' in col_lower or 'timestamp' in col_lower:
                        analysis["column_mappings"]["campaigns"]["date"] = col
                    elif 'spend' in col_lower or 'cost' in col_lower:
                        analysis["column_mappings"]["campaigns"]["spend"] = col
                    elif 'channel' in col_lower or 'source' in col_lower:
                        analysis["column_mappings"]["campaigns"]["channel"] = col
                    elif 'acquisition' in col_lower or 'conversion' in col_lower:
                        analysis["column_mappings"]["campaigns"]["acquisitions"] = col
            
            # Check for targets
            elif any(keyword in ' '.join(columns) for keyword in ['target', 'metric', 'goal', 'kpi']):
                analysis["targets_sheet"] = sheet_name
                # Map columns
                for col in df.columns:
                    col_lower = col.lower()
                    if 'metric' in col_lower or 'name' in col_lower:
                        analysis["column_mappings"]["targets"]["metric_name"] = col
                    elif 'value' in col_lower or 'target' in col_lower:
                        analysis["column_mappings"]["targets"]["value"] = col
        
        return analysis
    
    def process_excel_with_llm(self, file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Process Excel file using LLM analysis
        """
        print("🤖 Using LLM-powered Excel analysis...")
        
        # Analyze structure
        analysis = self.analyze_excel_structure(file_path)
        print(f"📊 LLM Analysis: {analysis}")
        
        # Read Excel data
        excel_data = pd.read_excel(file_path, sheet_name=None)
        
        # Process each sheet type
        transactions_df = self.process_transactions_sheet(excel_data, analysis)
        campaigns_df = self.process_campaigns_sheet(excel_data, analysis)
        targets_df = self.process_targets_sheet(excel_data, analysis)
        
        return transactions_df, campaigns_df, targets_df
    
    def process_transactions_sheet(self, excel_data: Dict[str, pd.DataFrame], analysis: Dict[str, Any]) -> pd.DataFrame:
        """
        Process transactions sheet based on LLM analysis
        """
        sheet_name = analysis.get("transactions_sheet")
        if not sheet_name or sheet_name not in excel_data:
            # Create default transactions
            return pd.DataFrame({
                'date': pd.to_datetime(['2023-01-01']),
                'description': ['Default Transaction'],
                'category': ['Revenue'],
                'amount': [1000.0]
            })
        
        df = excel_data[sheet_name].copy()
        mappings = analysis["column_mappings"]["transactions"]
        
        # Apply column mappings
        result_df = pd.DataFrame()
        
        if mappings.get("date"):
            result_df['date'] = pd.to_datetime(df[mappings["date"]], errors='coerce')
        else:
            result_df['date'] = pd.to_datetime(['2023-01-01'] * len(df))
        
        if mappings.get("amount"):
            result_df['amount'] = pd.to_numeric(df[mappings["amount"]], errors='coerce')
        else:
            result_df['amount'] = [1000.0] * len(df)
        
        if mappings.get("description"):
            result_df['description'] = df[mappings["description"]].astype(str)
        else:
            result_df['description'] = [f"Transaction {i+1}" for i in range(len(df))]
        
        if mappings.get("category"):
            result_df['category'] = df[mappings["category"]].astype(str)
        else:
            result_df['category'] = ['Revenue'] * len(df)
        
        # Clean data
        result_df = result_df.dropna(subset=['amount'])
        
        print(f"✅ Processed {len(result_df)} transactions from {sheet_name}")
        return result_df
    
    def process_campaigns_sheet(self, excel_data: Dict[str, pd.DataFrame], analysis: Dict[str, Any]) -> pd.DataFrame:
        """
        Process campaigns sheet based on LLM analysis
        """
        sheet_name = analysis.get("campaigns_sheet")
        if not sheet_name or sheet_name not in excel_data:
            # Create default campaigns
            return pd.DataFrame({
                'timestamp': pd.to_datetime(['2023-01-01']),
                'campaign_id': ['CAMP_001'],
                'channel': ['Google Ads'],
                'spend': [1000.0],
                'acquisitions': [10]
            })
        
        df = excel_data[sheet_name].copy()
        mappings = analysis["column_mappings"]["campaigns"]
        
        # Apply column mappings
        result_df = pd.DataFrame()
        
        if mappings.get("date"):
            result_df['timestamp'] = pd.to_datetime(df[mappings["date"]], errors='coerce')
        else:
            result_df['timestamp'] = pd.to_datetime(['2023-01-01'] * len(df))
        
        if mappings.get("spend"):
            result_df['spend'] = pd.to_numeric(df[mappings["spend"]], errors='coerce')
        else:
            result_df['spend'] = [1000.0] * len(df)
        
        if mappings.get("channel"):
            result_df['channel'] = df[mappings["channel"]].astype(str)
        else:
            result_df['channel'] = ['Default Channel'] * len(df)
        
        if mappings.get("acquisitions"):
            result_df['acquisitions'] = pd.to_numeric(df[mappings["acquisitions"]], errors='coerce')
        else:
            result_df['acquisitions'] = [10] * len(df)
        
        # Add campaign_id if not present
        result_df['campaign_id'] = [f"CAMP_{i+1:04d}" for i in range(len(result_df))]
        
        # Clean data
        result_df = result_df.dropna(subset=['spend'])
        
        print(f"✅ Processed {len(result_df)} campaigns from {sheet_name}")
        return result_df
    
    def process_targets_sheet(self, excel_data: Dict[str, pd.DataFrame], analysis: Dict[str, Any]) -> pd.DataFrame:
        """
        Process targets sheet based on LLM analysis
        """
        sheet_name = analysis.get("targets_sheet")
        if not sheet_name or sheet_name not in excel_data:
            # Create default targets
            return pd.DataFrame({
                'metric_name': ['Revenue Target', 'Cost Target'],
                'value': [100000, 50000]
            })
        
        df = excel_data[sheet_name].copy()
        mappings = analysis["column_mappings"]["targets"]
        
        # Apply column mappings
        result_df = pd.DataFrame()
        
        if mappings.get("metric_name"):
            result_df['metric_name'] = df[mappings["metric_name"]].astype(str)
        else:
            result_df['metric_name'] = [f"Metric {i+1}" for i in range(len(df))]
        
        if mappings.get("value"):
            result_df['value'] = pd.to_numeric(df[mappings["value"]], errors='coerce')
        else:
            result_df['value'] = [1000.0] * len(df)
        
        # Clean data
        result_df = result_df.dropna(subset=['value'])
        
        print(f"✅ Processed {len(result_df)} targets from {sheet_name}")
        return result_df

def load_data_from_excel_llm(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Main function to load Excel data using LLM analysis
    """
    processor = LLMExcelProcessor()
    return processor.process_excel_with_llm(file_path)

if __name__ == "__main__":
    # Test the LLM processor
    test_file = "dataset_1_saas_subscriptions.xlsx"
    if os.path.exists(test_file):
        transactions, campaigns, targets = load_data_from_excel_llm(test_file)
        print(f"\n📊 Results:")
        print(f"Transactions: {len(transactions)} rows")
        print(f"Campaigns: {len(campaigns)} rows") 
        print(f"Targets: {len(targets)} rows")
        print(f"\nSample transactions:")
        print(transactions.head())
    else:
        print(f"Test file {test_file} not found")
