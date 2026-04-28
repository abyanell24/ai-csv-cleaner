import pandas as pd
import numpy as np
import re
from datetime import datetime
from collections import Counter


def standardize_date(val):
    """Standardize date to YYYY-MM-DD format"""
    if pd.isna(val) or str(val).strip() in ['', 'N/A', 'null', 'None', 'nan']:
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


def fix_zero_age(val):
    """Fix zero values in Age column"""
    if pd.isna(val) or val == '':
        return ''
    try:
        if float(val) == 0:
            return ''
    except:
        pass
    return val


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


def fill_missing_numeric(series, fill_value=None):
    """Fill missing numeric values with median"""
    if fill_value is not None:
        return series.fillna(fill_value)
    
    valid = pd.to_numeric(series, errors='coerce').dropna()
    if len(valid) > 0:
        return series.fillna(valid.median())
    return series.fillna(0)


def fill_missing_categorical(series):
    """Fill missing categorical values with mode"""
    valid = series[series != ''].dropna()
    if len(valid) > 0:
        counter = Counter(valid)
        return series.fillna(counter.most_common(1)[0][0])
    return series.fillna('unknown')


def remove_duplicates(df):
    """Remove duplicate rows"""
    return df.drop_duplicates()


def comprehensive_clean(df):
    """Comprehensive cleaning Pipeline"""
    
    # Step 1: Basic string conversion
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else '')
    
    # Step 2: Remove duplicates
    df = remove_duplicates(df)
    
    # Step 3: Identify column types
    col_lower = {col: col.lower() for col in df.columns}
    
    # Date columns
    date_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['date', 'join', 'birth', 'start'])]
    for col in date_cols:
        df[col] = df[col].apply(lambda x: standardize_date(x) if x else '')
    
    # Age column - fix zeros
    age_cols = [col for col in df.columns if 'age' in col_lower[col]]
    for col in age_cols:
        df[col] = df[col].apply(lambda x: fix_zero_age(x) if x else '')
        df[col] = fill_missing_numeric(df[col])
    
    # Phone columns - fix negatives
    phone_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['phone', 'telepon', 'hp'])]
    for col in phone_cols:
        df[col] = df[col].apply(lambda x: fix_negative_phone(x) if x else '')
    
    # Categorical columns - normalize case (except emails)
    email_cols = [col for col in df.columns if 'email' in col_lower[col]]
    categorical_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['category', 'department', 'status', 'role', 'type', 'gender', 'region']) and col not in email_cols]
    for col in categorical_cols:
        df[col] = df[col].apply(lambda x: standardize_case(x) if x else '')
        df[col] = fill_missing_categorical(df[col])
    
    # Name columns - normalize case
    name_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['name', 'first', 'last'])]
    for col in name_cols:
        df[col] = df[col].apply(lambda x: standardize_case(x) if x else '')
    
    # Salary/Pay columns - fix zeros and fill missing
    salary_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['salary', 'pay', 'wage', 'harga'])]
    for col in salary_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Replace zeros with median
        median_val = df[col][df[col] > 0].median() if len(df[col][df[col] > 0]) > 0 else 0
        df[col] = df[col].replace(0, median_val)
        df[col] = df[col].fillna(median_val)
        df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else '')
    
    # Numeric columns - fill missing with median
    numeric_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['quantity', 'qty', 'score', 'point']) and col not in date_cols + age_cols + salary_cols]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = fill_missing_numeric(df[col])
        df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else '')
    
    # Boolean columns - standardize
    bool_cols = [col for col in df.columns if any(x in col_lower[col] for x in ['remote', 'active', 'status'])]
    for col in bool_cols:
        df[col] = df[col].apply(lambda x: str(x).lower() if x else '')
        df[col] = df[col].replace({'1': 'true', '0': 'false', 'yes': 'true', 'no': 'false', 'true': 'true', 'false': 'false'})
    
    # Fill remaining empty with 'unknown'
    for col in df.columns:
        df[col] = df[col].replace('', 'unknown')
    
    return df


def detect_and_fix_duplicate_columns(df):
    cols = df.columns.tolist()
    seen = {}
    new_cols = []
    
    for col in cols:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    
    df.columns = new_cols
    return df


def fix_shifted_rows(df):
    rows_to_fix = []
    for idx, row in df.iterrows():
        first_val = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        if first_val == "" or first_val.startswith(","):
            rows_to_fix.append(idx)
    
    return df, rows_to_fix


def standardize_dates_in_column(series):
    def parse_date(val):
        if pd.isna(val) or str(val).strip() in ["", "N/A", "null", "abc", "N/A"]:
            return None
        
        val_str = str(val).strip()
        
        formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%b %d %Y",
            "%b %d, %Y",
            "%d-%m-%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(val_str, fmt).strftime("%Y-%m-%d")
            except:
                continue
        
        return None
    
    return series.apply(parse_date)


def convert_to_numeric(series):
    def parse_number(val):
        if pd.isna(val):
            return 0
        
        val_str = str(val).strip()
        
        if val_str in ["", "N/A", "null", "NaN", "nan", "None"]:
            return 0
        
        val_str = val_str.replace(",", "")
        
        number_map = {
            "abd": 0,
            "abc": 0,
            "four hundred": 400,
            "three hundred": 300,
            "two hundred": 200,
            "one hundred": 100,
            "a": 0,
            "n/a": 0,
        }
        
        if val_str.lower() in number_map:
            return number_map[val_str.lower()]
        
        symbols_to_remove = ["$", "€", "£", "%", ")", "(", "a", "b", "d"]
        for sym in symbols_to_remove:
            val_str = val_str.replace(sym, "")
        
        val_str = val_str.strip()
        
        try:
            return float(val_str)
        except:
            return 0
    
    return series.apply(parse_number)


def standardize_text(series):
    def parse_text(val):
        if pd.isna(val):
            return ""
        
        val_str = str(val).strip()
        
        if val_str in ["", "N/A", "null", "NaN", "nan", "None", "nan"]:
            return ""
        
        return val_str.strip()
    
    return series.apply(parse_text)


def standardize_category(series):
    series = standardize_text(series)
    
    category_map = {
        "electronics": "electronics",
        "electronic": "electronics",
        "ELECTRONICS": "electronics",
        "sports": "sports",
        "Sports": "sports",
        "SPORTS": "sports",
        "books": "books",
        "Books": "books",
        "BOOKS": "books",
        "home": "home",
        "Home": "home",
        "HOME": "home",
        "clothing": "clothing",
        "Clothing": "clothing",
        "CLOTHING": "clothing",
    }
    
    return series.apply(lambda x: category_map.get(x.lower(), x.lower()) if x else "")


def standardize_status(series):
    series = standardize_text(series)
    
    status_map = {
        "delivered": "delivered",
        "Delivered": "delivered",
        "DELIVERED": "delivered",
        "shipped": "shipped",
        "Shipped": "shipped",
        "processing": "processing",
        "Processing": "processing",
        "returned": "returned",
        "Returned": "returned",
        "cancelled": "cancelled",
        "Cancelled": "cancelled",
    }
    
    return series.apply(lambda x: status_map.get(x.lower(), x.lower()) if x else "")


def normalize_dtypes(df):
    """Normalize column dtypes - convert all to strings using apply"""
    for col in df.columns:
        df[col] = df[col].fillna('').apply(lambda x: str(x) if pd.notna(x) else '')
    return df


def recalculate_total(df, quantity_col, price_col, total_col):
    if quantity_col in df.columns and price_col in df.columns:
        df[total_col] = df[quantity_col] * df[price_col]
    return df


def remove_duplicates(df):
    return df.drop_duplicates()


def validate_and_fix_dataframe(df):
    # Convert all to string using apply
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else '')
    
    return df


def pre_process_csv(file):
    # Read and convert all to strings using apply
    df = pd.read_csv(file)
    df = df.fillna('')
    
    df = detect_and_fix_duplicate_columns(df)
    
    # Convert each value to string properly
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else '')
    
    return df


def post_process_dataframe(df):
    df = normalize_dtypes(df)
    df = remove_duplicates(df)
    
    # Fill missing values with context before recalculating totals
    df = fill_missing_with_context(df)
    
    qty_cols = [c for c in df.columns if "quantity" in c.lower() or "qty" in c.lower()]
    price_cols = [c for c in df.columns if "price" in c.lower()]
    total_cols = [c for c in df.columns if "total" in c.lower()]
    
    if qty_cols and price_cols and total_cols:
        df = recalculate_total(df, qty_cols[0], price_cols[0], total_cols[0])
    
    df = normalize_dtypes(df)
    
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = standardize_text(df[col])
    
    return df


def clean_csv_pipeline(file):
    df = pre_process_csv(file)
    
    return df.to_dict(orient="records")


def clean_csv_full_pipeline(file):
    df = pd.read_csv(file)
    
    df = detect_and_fix_duplicate_columns(df)
    
    df = validate_and_fix_dataframe(df)
    
    df = remove_duplicates(df)
    
    df = post_process_dataframe(df)
    
    return df