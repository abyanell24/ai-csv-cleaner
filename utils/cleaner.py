import pandas as pd
import numpy as np
import re
from datetime import datetime
from collections import Counter


def detect_column_type(series):
    """Detect column type based on content"""
    
    # Get non-empty values
    valid_vals = series[series != ''].dropna()
    if len(valid_vals) == 0:
        return "empty"
    
    # Check for date patterns
    date_formats = [
        '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
        '%b %d %Y', '%b %d, %Y', '%d-%m-%Y', '%m-%d-%Y'
    ]
    date_count = 0
    for fmt in date_formats:
        try:
            dates = pd.to_datetime(valid_vals, format=fmt, errors='raise')
            date_count = dates.notna().sum()
            break
        except:
            try:
                dates = pd.to_datetime(valid_vals, errors='coerce')
                date_count = dates.notna().sum()
            except:
                pass
    
    if date_count > len(valid_vals) * 0.7:
        return "date"
    
    # Check for boolean patterns
    bool_patterns = ['true', 'false', 'yes', 'no', '1', '0']
    bool_count = sum(1 for v in valid_vals.str.lower() if str(v).lower() in bool_patterns)
    if bool_count > len(valid_vals) * 0.5:
        return "boolean"
    
    # Check for numeric
    try:
        numeric = pd.to_numeric(valid_vals, errors='coerce')
        if numeric.notna().sum() > len(valid_vals) * 0.8:
            # Check if it's age (typically 18-100) or typical number
            return "numeric"
    except:
        pass
    
    # Check for email
    if sum(1 for v in valid_vals if '@' in str(v) and '.' in str(v)) > len(valid_vals) * 0.5:
        return "email"
    
    # Check for phone (digits only, 10-15 chars)
    phone_pattern = re.compile(r'^\d{10,15}$')
    if sum(1 for v in valid_vals if phone_pattern.match(str(v).replace('-', '').replace(' ', ''))) > len(valid_vals) * 0.5:
        return "phone"
    
    # Check for category (low unique ratio)
    unique_ratio = len(valid_vals.unique()) / len(valid_vals)
    if unique_ratio < 0.3:
        return "categorical"
    
    return "text"


def standardize_date(val):
    """Standardize date to YYYY-MM-DD format"""
    if pd.isna(val) or str(val).strip() in ['', 'N/A', 'null', 'None', 'nan', 'NaN']:
        return ''
    
    val_str = str(val).strip()
    
    formats = [
        '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
        '%b %d %Y', '%b %d, %Y', '%d-%m-%Y', '%m-%d-%Y'
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(val_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except:
            continue
    
    return val_str


def standardize_case(val):
    """Standardize case and trim whitespace"""
    if pd.isna(val):
        return ''
    return str(val).strip().lower()


def fix_negative_phone(val):
    """Fix negative phone numbers"""
    if pd.isna(val):
        return ''
    val_str = str(val).strip()
    # Remove negative sign and any leading garbage
    if val_str.startswith('-'):
        val_str = val_str.lstrip('-')
    # Keep only digits
    digits = re.sub(r'\D', '', val_str)
    return digits if digits else ''


def auto_clean_column(series, col_type):
    """Apply cleaning based on detected type"""
    
    if col_type == "empty":
        return series.fillna('unknown')
    
    elif col_type == "date":
        return series.apply(lambda x: standardize_date(x) if x else '')
    
    elif col_type == "boolean":
        return series.str.lower().replace({
            'true': 'true', 'false': 'false', 
            'yes': 'true', 'no': 'false',
            '1': 'true', '0': 'false'
        })
    
    elif col_type == "phone":
        return series.apply(lambda x: fix_negative_phone(x) if x else '')
    
    elif col_type == "numeric":
        # Convert to numeric, replace zeros with median
        numeric = pd.to_numeric(series, errors='coerce')
        median_val = numeric[numeric > 0].median() if len(numeric[numeric > 0]) > 0 else 0
        numeric = numeric.replace(0, median_val)
        numeric = numeric.fillna(median_val)
        return numeric.apply(lambda x: str(x) if pd.notna(x) else '')
    
    elif col_type == "categorical":
        # Fill missing with mode and lowercase
        mode_val = series[series != ''].mode()
        filled = series.fillna(mode_val[0] if len(mode_val) > 0 else 'unknown')
        return filled.apply(lambda x: standardize_case(x) if x else '')
    
    elif col_type == "email":
        return series.str.lower().apply(lambda x: str(x).strip() if x else '')
    
    else:  # text
        return series.apply(lambda x: standardize_case(x) if x else '')


def auto_clean(df):
    """Main auto-cleaning function"""
    
    # Step 1: Basic string conversion
    for col in df.columns:
        df[col] = df[col].fillna('').astype(str)
    
    # Step 2: Remove duplicates
    df = df.drop_duplicates()
    
    # Step 3: Detect and clean each column
    cleaned_columns = {}
    for col in df.columns:
        col_type = detect_column_type(df[col])
        cleaned_columns[col] = auto_clean_column(df[col], col_type)
    
    # Apply cleaned columns
    for col, cleaned in cleaned_columns.items():
        df[col] = cleaned
    
    # Step 4: Fill any remaining empty cells with 'unknown'
    for col in df.columns:
        df[col] = df[col].replace('', 'unknown')
    
    return df


def comprehensive_clean(df):
    """Wrapper for backward compatibility"""
    return auto_clean(df)


def pre_process_csv(file):
    """Read and pre-process CSV"""
    df = pd.read_csv(file)
    return df


def validate_and_fix_dataframe(df):
    """Legacy wrapper"""
    return auto_clean(df)


def fill_missing_with_context(df):
    """Legacy wrapper"""
    return auto_clean(df)


def normalize_dtypes(df):
    """Legacy wrapper"""
    return auto_clean(df)


def post_process_dataframe(df):
    """Legacy wrapper"""
    return auto_clean(df)