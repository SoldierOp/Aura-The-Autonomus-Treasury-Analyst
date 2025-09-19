#!/usr/bin/env python3
"""
Interactive Excel Processor
Handles user requirements and modifies Excel files accordingly
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import requests
from config import GEMINI_API_KEY, GEMINI_API_URL
import tempfile
import os

class InteractiveExcelProcessor:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
        self.user_requirements = {}
        self.original_data = {}
        
    def analyze_excel_and_ask_questions(self, filepath: str) -> dict:
        """
        Analyze uploaded Excel and generate relevant questions
        """
        try:
            # Load the Excel file
            excel_file = pd.ExcelFile(filepath)
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                sheets_data[sheet_name] = {
                    'data': df,
                    'columns': list(df.columns),
                    'rows': len(df),
                    'sample_data': df.head(3).to_dict('records')
                }
            
            self.original_data = sheets_data
            
            # Generate questions based on the data
            questions = self._generate_questions(sheets_data)
            
            return {
                'status': 'success',
                'file_info': {
                    'filename': os.path.basename(filepath),
                    'sheets': list(sheets_data.keys()),
                    'total_rows': sum(sheet['rows'] for sheet in sheets_data.values())
                },
                'questions': questions,
                'data_summary': self._create_data_summary(sheets_data)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error analyzing Excel: {str(e)}'
            }
    
    def _generate_questions(self, sheets_data: dict) -> list:
        """
        Generate relevant questions based on Excel content
        """
        questions = []
        
        # General questions
        questions.append({
            'id': 'output_format',
            'question': 'What format do you want for the output Excel file?',
            'type': 'multiple_choice',
            'options': [
                'Same structure with modifications',
                'Consolidated single sheet',
                'New structure with specific columns',
                'Summary report format'
            ],
            'required': True
        })
        
        # Data modification questions
        questions.append({
            'id': 'data_modifications',
            'question': 'What data modifications do you want?',
            'type': 'multiple_choice',
            'options': [
                'Add calculated columns',
                'Filter specific data',
                'Aggregate/summarize data',
                'Sort data by specific criteria',
                'Remove duplicate entries',
                'No modifications needed'
            ],
            'required': True
        })
        
        # Specific questions based on detected data
        for sheet_name, sheet_info in sheets_data.items():
            columns = sheet_info['columns']
            
            # If there are date columns
            if any('date' in col.lower() or 'time' in col.lower() for col in columns):
                questions.append({
                    'id': f'date_filter_{sheet_name}',
                    'question': f'Do you want to filter {sheet_name} by date range?',
                    'type': 'yes_no',
                    'required': False
                })
            
            # If there are amount/price columns
            if any('amount' in col.lower() or 'price' in col.lower() or 'cost' in col.lower() for col in columns):
                questions.append({
                    'id': f'amount_filter_{sheet_name}',
                    'question': f'Do you want to filter {sheet_name} by amount range?',
                    'type': 'yes_no',
                    'required': False
                })
            
            # If there are category columns
            if any('category' in col.lower() or 'type' in col.lower() or 'status' in col.lower() for col in columns):
                questions.append({
                    'id': f'category_filter_{sheet_name}',
                    'question': f'Do you want to filter {sheet_name} by specific categories?',
                    'type': 'yes_no',
                    'required': False
                })
        
        # Calculation questions
        questions.append({
            'id': 'calculations',
            'question': 'What calculations do you want to add?',
            'type': 'multiple_choice',
            'options': [
                'Totals and subtotals',
                'Percentage calculations',
                'Growth rates',
                'Averages and medians',
                'Custom formulas',
                'No calculations needed'
            ],
            'required': False
        })
        
        # Output preferences
        questions.append({
            'id': 'output_preferences',
            'question': 'Any specific output preferences?',
            'type': 'multiple_choice',
            'options': [
                'Include charts/graphs',
                'Add data validation',
                'Format as table',
                'Add conditional formatting',
                'Standard formatting only'
            ],
            'required': False
        })
        
        return questions
    
    def _create_data_summary(self, sheets_data: dict) -> dict:
        """
        Create a summary of the Excel data
        """
        summary = {
            'total_sheets': len(sheets_data),
            'total_rows': sum(sheet['rows'] for sheet in sheets_data.values()),
            'sheets_info': {}
        }
        
        for sheet_name, sheet_info in sheets_data.items():
            summary['sheets_info'][sheet_name] = {
                'rows': sheet_info['rows'],
                'columns': len(sheet_info['columns']),
                'column_names': sheet_info['columns']
            }
        
        return summary
    
    def process_user_requirements(self, requirements: dict) -> dict:
        """
        Process user requirements and generate modified Excel
        """
        try:
            self.user_requirements = requirements
            
            # Process each sheet based on requirements
            modified_sheets = {}
            
            for sheet_name, sheet_info in self.original_data.items():
                modified_df = self._process_sheet(sheet_name, sheet_info['data'], requirements)
                modified_sheets[sheet_name] = modified_df
            
            # Generate output file
            output_filepath = self._create_output_file(modified_sheets, requirements)
            
            return {
                'status': 'success',
                'output_file': output_filepath,
                'modifications_applied': self._get_modifications_summary(requirements),
                'file_info': {
                    'original_rows': sum(sheet['rows'] for sheet in self.original_data.values()),
                    'modified_rows': sum(len(df) for df in modified_sheets.values()),
                    'sheets_processed': len(modified_sheets)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error processing requirements: {str(e)}'
            }
    
    def _process_sheet(self, sheet_name: str, df: pd.DataFrame, requirements: dict) -> pd.DataFrame:
        """
        Process individual sheet based on requirements
        """
        modified_df = df.copy()
        
        # Apply filters
        if requirements.get('data_modifications') == 'Filter specific data':
            modified_df = self._apply_filters(modified_df, sheet_name, requirements)
        
        # Add calculations
        if requirements.get('calculations'):
            modified_df = self._add_calculations(modified_df, requirements)
        
        # Sort data
        if requirements.get('data_modifications') == 'Sort data by specific criteria':
            modified_df = self._apply_sorting(modified_df, requirements)
        
        # Remove duplicates
        if requirements.get('data_modifications') == 'Remove duplicate entries':
            modified_df = modified_df.drop_duplicates()
        
        return modified_df
    
    def _apply_filters(self, df: pd.DataFrame, sheet_name: str, requirements: dict) -> pd.DataFrame:
        """
        Apply filters based on requirements
        """
        filtered_df = df.copy()
        
        # Date filters
        date_filter_key = f'date_filter_{sheet_name}'
        if requirements.get(date_filter_key) == 'yes':
            date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_columns:
                # Apply default date range (last 30 days)
                date_col = date_columns[0]
                if pd.api.types.is_datetime64_any_dtype(df[date_col]):
                    cutoff_date = datetime.now() - timedelta(days=30)
                    filtered_df = filtered_df[filtered_df[date_col] >= cutoff_date]
        
        # Amount filters
        amount_filter_key = f'amount_filter_{sheet_name}'
        if requirements.get(amount_filter_key) == 'yes':
            amount_columns = [col for col in df.columns if any(word in col.lower() for word in ['amount', 'price', 'cost'])]
            if amount_columns:
                amount_col = amount_columns[0]
                # Filter for positive amounts only
                filtered_df = filtered_df[filtered_df[amount_col] > 0]
        
        # Category filters
        category_filter_key = f'category_filter_{sheet_name}'
        if requirements.get(category_filter_key) == 'yes':
            category_columns = [col for col in df.columns if any(word in col.lower() for word in ['category', 'type', 'status'])]
            if category_columns:
                category_col = category_columns[0]
                # Remove empty categories
                filtered_df = filtered_df[filtered_df[category_col].notna()]
        
        return filtered_df
    
    def _add_calculations(self, df: pd.DataFrame, requirements: dict) -> pd.DataFrame:
        """
        Add calculated columns based on requirements
        """
        modified_df = df.copy()
        
        calculations = requirements.get('calculations', [])
        
        if 'Totals and subtotals' in calculations:
            # Add row totals for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                modified_df['Row_Total'] = modified_df[numeric_cols].sum(axis=1)
        
        if 'Percentage calculations' in calculations:
            # Add percentage columns
            amount_cols = [col for col in df.columns if 'amount' in col.lower()]
            if amount_cols:
                total_amount = modified_df[amount_cols[0]].sum()
                modified_df['Amount_Percentage'] = (modified_df[amount_cols[0]] / total_amount * 100).round(2)
        
        if 'Growth rates' in calculations:
            # Add growth rate calculations
            date_cols = [col for col in df.columns if 'date' in col.lower()]
            amount_cols = [col for col in df.columns if 'amount' in col.lower()]
            
            if date_cols and amount_cols:
                modified_df = modified_df.sort_values(date_cols[0])
                modified_df['Growth_Rate'] = modified_df[amount_cols[0]].pct_change() * 100
        
        if 'Averages and medians' in calculations:
            # Add statistical columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                modified_df['Average_Value'] = modified_df[numeric_cols].mean(axis=1)
                modified_df['Median_Value'] = modified_df[numeric_cols].median(axis=1)
        
        return modified_df
    
    def _apply_sorting(self, df: pd.DataFrame, requirements: dict) -> pd.DataFrame:
        """
        Apply sorting based on requirements
        """
        # Default sorting by date if available
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if date_cols:
            return df.sort_values(date_cols[0], ascending=False)
        
        # Sort by amount if available
        amount_cols = [col for col in df.columns if 'amount' in col.lower()]
        if amount_cols:
            return df.sort_values(amount_cols[0], ascending=False)
        
        return df
    
    def _create_output_file(self, modified_sheets: dict, requirements: dict) -> str:
        """
        Create output Excel file
        """
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_file.close()
        
        with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
            for sheet_name, df in modified_sheets.items():
                # Apply formatting based on requirements
                if requirements.get('output_preferences') == 'Format as table':
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return temp_file.name
    
    def _get_modifications_summary(self, requirements: dict) -> list:
        """
        Get summary of modifications applied
        """
        modifications = []
        
        if requirements.get('data_modifications'):
            modifications.append(f"Data modifications: {requirements['data_modifications']}")
        
        if requirements.get('calculations'):
            modifications.append(f"Calculations added: {requirements['calculations']}")
        
        if requirements.get('output_format'):
            modifications.append(f"Output format: {requirements['output_format']}")
        
        return modifications

# Main function for integration
def process_excel_interactively(filepath: str, requirements: dict = None) -> dict:
    """
    Main function to process Excel files interactively
    """
    processor = InteractiveExcelProcessor()
    
    if requirements is None:
        # First call - analyze and ask questions
        return processor.analyze_excel_and_ask_questions(filepath)
    else:
        # Second call - process based on requirements
        return processor.process_user_requirements(requirements)
