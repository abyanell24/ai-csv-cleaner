# AI CSV Cleaner

A powerful web application for parsing, cleaning, and transforming CSV data using AI. Built with Streamlit and Cerebras AI.

## Features

- **CSV Parser**: Convert CSV to JSON format with AI-powered analysis
- **CSV Cleaner**: Clean and standardize CSV data using AI + Python preprocessing
  - Automatic duplicate removal
  - Missing value imputation (median/mode-based)
  - Data type fixing (text to numbers, date standardization)
  - Duplicate column detection and fixing
  - Text standardization (lowercase, trim whitespace)
  - Total recalculation for calculated fields
- **Batch Processing**: Handle large CSV files in batches
- **Progress Tracking**: Real-time progress bars during processing
- **Export**: Download cleaned data as CSV or JSON

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI | Cerebras (llama-3.1-8b) |
| Language | Python 3.9+ |
| Processing | Pandas + NumPy |

## Architecture

```
User Upload CSV
      ↓
Pre-Processing (Python)
      ↓  - Duplicate column detection
      ↓  - Data type fixing
      ↓  - Missing value imputation
      ↓  - Date standardization
      ↓
AI Cleaning (Cerebras)
      ↓  - Batch processing (50 rows/batch)
      ↓  - Content standardization
      ↓
Post-Processing (Python)
      ↓  - Duplicate removal
      ↓  - Recalculate totals
      ↓  - Final validation
      ↓
Download Cleaned CSV
```

## Quick Start

### Local Installation

```bash
# Clone the repository
git clone https://github.com/abyanell24/ai-csv-cleaner.git
cd ai-csv-cleaner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Open in Browser

Navigate to: `http://localhost:8501`

## API Keys

This application uses Cerebras AI for inference. No API key is required for the free tier as the key is already embedded in the codebase.

For production use, you may want to set your own API key. See [API.md](./API.md) for details.

## Usage

### CSV Parser Tab

1. Upload a CSV file
2. View data preview and info
3. Optionally enable AI analysis
4. Download JSON output

### CSV Cleaner Tab

1. Upload a CSV file (any type: sales, inventory, population, etc.)
2. View data preview
3. Click "Clean with AI"
4. Wait for processing (progress bar shows batch status)
5. Download cleaned CSV

## Data Cleaning Rules

The cleaner applies industry-standard rules:

1. **Missing Values**: Filled with median (numeric) or mode (categorical)
2. **Data Types**: Text numbers converted (e.g., "abd" → 0, "$300" → 300)
3. **Dates**: Standardized to YYYY-MM-DD format
4. **Duplicates**: Automatically removed
5. **Categories**: Lowercase standardized
6. **Totals**: Recalculated if quantity and price exist

## License

MIT License - See [LICENSE](../LICENSE)

## Author

- **GitHub**: [abyanell24](https://github.com/abyanell24)

---

For detailed installation instructions, see [INSTALL.md](./INSTALL.md)

For usage guide, see [USAGE.md](./USAGE.md)