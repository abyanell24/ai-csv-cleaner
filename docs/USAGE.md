# Usage Guide

This guide explains how to use the AI CSV Cleaner application.

## Overview

The application has two main tabs:

| Tab | Function |
|-----|----------|
| CSV Parser | Convert CSV to JSON |
| CSV Cleaner | Clean and standardize CSV data |

---

## Using CSV Parser

### Step 1: Upload CSV

1. Open the application in your browser
2. Go to the **CSV Parser** tab
3. Click "Choose file CSV" to upload your CSV file
4. Wait for the file to load

### Step 2: View Data

After upload, you will see:

- **Preview Data**: First 10 rows displayed in a table
- **CSV Info**: Column names, row count, and data types

### Step 3: AI Analysis (Optional)

1. Check the "Analyze with AI" checkbox
2. Click "Run AI Analysis"
3. Wait for the AI to analyze your data
4. View the analysis result

### Step 4: Download JSON

1. Scroll to the JSON Output section
2. Click "Download JSON" button

---

## Using CSV Cleaner

### Step 1: Upload CSV

1. Go to the **CSV Cleaner** tab
2. Click "Choose file CSV to clean"
3. Select your CSV file

### Step 2: Preview Data

View the original data before cleaning:

- First 10 rows displayed
- Row count shown

### Step 3: Clean Data

1. Click **"Clean with AI"** button
2. Wait for processing (progress bar shows status)

Processing steps:
- Step 1: Pre-processing (15%)
- Step 2: AI cleaning (15-85%)
- Step 3: Post-processing (85-100%)

### Step 4: Download Cleaned CSV

1. Wait for processing to complete
2. View the cleaned data preview
3. Click **"Download CSV_cleaned.csv"** button

---

## Supported CSV Types

The cleaner works with various CSV types:

| Type | Examples |
|------|----------|
| Sales data | Orders, transactions |
| Inventory | Products, stock |
| Population | Demographics, census |
| Employees | HR records |
| Customers | Customer lists |

---

## Cleaning Rules Applied

The application applies these industry-standard cleaning rules:

### 1. Duplicate Column Detection
- Fixes duplicate column names (e.g., "Category" appearing twice)

### 2. Missing Value Imputation
- Numeric columns: Filled with median value
- Categorical columns: Filled with mode (most frequent)
- Text columns: Filled with most common value

### 3. Data Type Fixing
- Text numbers converted: "abd" → 0, "four hundred" → 400
- Currency cleaned: "$300" → 300
- Invalid values: Set to 0

### 4. Date Standardization
- All dates converted to YYYY-MM-DD format

### 5. Duplicate Removal
- Identical rows removed

### 6. Text Standardization
- Lowercase for categories
- Trimmed whitespace

### 7. Total Recalculation
- Total = Quantity × Price (if those columns exist)

---

## Tips for Best Results

| Tip | Description |
|-----|-------------|
| UTF-8 encoding | Ensure your CSV uses UTF-8 encoding |
| Headers | First row should contain column names |
| Consistent columns | Each row should have the same number of columns |
| Date formats | Any date format will be standardized |

---

## Troubleshooting

### "Error: No columns to parse"

**Cause**: Corrupted or empty CSV file

**Solution**: Check your CSV file format

### Processing takes long time

**Cause**: Large CSV files are processed in batches

**Solution**: This is normal. Progress bar shows the status.

### Missing values not filled

**Cause**: May happen if all values in a column are missing

**Solution**: The cleaner tries best effort imputation

---

## Next Steps

After cleaning, you can:

1. Download cleaned CSV
2. Use in other applications
3. Import to databases

For API information, see [API.md](./API.md).