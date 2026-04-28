import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
from collections import Counter


def detect_column_type(col_name, df):
    """Detect jenis kolom berdasarkan nama dan data"""
    col_lower = col_name.lower()
    
    # Numeric columns
    if any(x in col_lower for x in ["quantity", "qty", "price", "amount", "total", "cost", "harga", "nomor", "usia", "age", "score", "point"]):
        return "numeric"
    
    # Date columns
    if any(x in col_lower for x in ["date", "tanggal", "waktu", "time", "tgl", "born", "lahir"]):
        return "date"
    
    # Categorical columns
    if any(x in col_lower for x in ["category", "kategori", "type", "jenis", "status", "condition", "kondisi", "gender", "sex", "role"]):
        return "categorical"
    
    # Email/Phone columns
    if any(x in col_lower for x in ["email", "phone", "telepon", "hp", "wa"]):
        return "contact"
    
    # Check data samples
    sample = df[col_name].dropna().head(20)
    if len(sample) > 0:
        # Check if numeric
        try:
            numeric_sample = pd.to_numeric(sample, errors='coerce')
            if numeric_sample.notna().sum() > len(sample) * 0.7:
                return "numeric"
        except:
            pass
        
        # Check if date
        try:
            date_sample = pd.to_datetime(sample, errors='coerce')
            if date_sample.notna().sum() > len(sample) * 0.7:
                return "date"
        except:
            pass
        
        # Check unique values ratio for categorical
        unique_ratio = len(sample.unique()) / len(sample)
        if unique_ratio < 0.5:
            return "categorical"
    
    return "text"


def fill_missing_with_context(df):
    """Fill missing values dengan mean/median/mode dari masing-masing kolom"""
    
    for col in df.columns:
        col_type = detect_column_type(col, df)
        missing_mask = df[col].isna() | (df[col] == "") | (df[col] == "N/A") | (df[col] == "null")
        
        if missing_mask.sum() == 0:
            continue
        
        if col_type == "numeric":
            # Fill dengan median (lebih robust dari mean untuk outliers)
            valid_vals = pd.to_numeric(df[col], errors='coerce')
            median_val = valid_vals.median()
            if pd.isna(median_val):
                median_val = 0
            df.loc[missing_mask, col] = median_val
            
        elif col_type == "categorical" or col_type == "text":
            # Fill dengan mode (most frequent)
            valid_vals = df.loc[~missing_mask, col].dropna()
            valid_vals = valid_vals[valid_vals != ""]
            
            if len(valid_vals) > 0:
                counter = Counter(valid_vals)
                mode_val = counter.most_common(1)[0][0]
                df.loc[missing_mask, col] = mode_val
            else:
                df.loc[missing_mask, col] = "Unknown"
                
        elif col_type == "date":
            # Fill dengan median date
            valid_dates = pd.to_datetime(df[col], errors='coerce')
            valid_dates = valid_dates[~valid_dates.isna()]
            
            if len(valid_dates) > 0:
                median_date = valid_dates.median()
                if pd.notna(median_date):
                    df.loc[missing_mask, col] = median_date.strftime("%Y-%m-%d")
                else:
                    df.loc[missing_mask, col] = datetime.now().strftime("%Y-%m-%d")
            else:
                df.loc[missing_mask, col] = datetime.now().strftime("%Y-%m-%d")
        
        elif col_type == "contact":
            # Fill dengan "Unknown" untuk contact
            df.loc[missing_mask, col] = "Unknown"
    
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
    """Normalize column dtypes - fix float to int where applicable"""
    for col in df.columns:
        if df[col].dtype == 'float64':
            try:
                valid_vals = df[col].dropna()
                if len(valid_vals) > 0 and (valid_vals == valid_vals.astype(int)).all():
                    df[col] = df[col].astype(int)
            except:
                pass
        elif df[col].dtype == 'object':
            df[col] = df[col].astype(str)
    return df


def recalculate_total(df, quantity_col, price_col, total_col):
    if quantity_col in df.columns and price_col in df.columns:
        df[total_col] = df[quantity_col] * df[price_col]
    return df


def remove_duplicates(df):
    return df.drop_duplicates()


def validate_and_fix_dataframe(df):
    numeric_cols = []
    text_cols = []
    date_cols = []
    category_cols = ["category", "categories", "type", "jenis", "kategori"]
    status_cols = ["status", "condition", "kondisi"]
    
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ["quantity", "qty", "price", "amount", "total", "cost", "harga"]):
            numeric_cols.append(col)
        elif any(x in col_lower for x in ["date", "tanggal", "waktu", "time"]):
            date_cols.append(col)
        elif any(x in col_lower for x in category_cols):
            category_cols.append(col)
        elif any(x in col_lower for x in status_cols):
            status_cols.append(col)
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = convert_to_numeric(df[col])
    
    for col in date_cols:
        if col in df.columns:
            df[col] = standardize_dates_in_column(df[col])
    
    for col in df.columns:
        if col not in numeric_cols and col not in date_cols:
            df[col] = standardize_text(df[col])
    
    for col in category_cols:
        if col in df.columns:
            df[col] = standardize_category(df[col])
    
    for col in status_cols:
        if col in df.columns:
            df[col] = standardize_status(df[col])
    
    df = fill_missing_with_context(df)
    
    return df


def pre_process_csv(file):
    df = pd.read_csv(file)
    
    df = detect_and_fix_duplicate_columns(df)
    
    df = validate_and_fix_dataframe(df)
    
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