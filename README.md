# AI CSV Cleaner

A powerful web application for parsing, cleaning, and transforming CSV data using AI. Built with Streamlit and Cerebras AI.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

## Quick Start

### Run Locally

```bash
# Clone the repository
git clone https://github.com/abyanell24/ai-csv-cleaner.git
cd ai-csv-cleaner

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open: **http://localhost:8501**

### Run Online

Deploy to Streamlit Community Cloud:

1. Go to https://share.streamlit.io
2. Connect your GitHub account
3. Select this repository
4. Deploy!

Your app will be available at: `https://ai-csv-cleaner.streamlit.app`

## Features

- **CSV Parser** - Convert CSV to JSON format with AI analysis
- **CSV Cleaner** - Clean and standardize any CSV data using AI
  - Automatic missing value imputation
  - Duplicate removal
  - Data type fixing
  - Date standardization
  - Category standardization
  - Total recalculation
- **Batch Processing** - Handle large files efficiently
- **Progress Tracking** - Real-time progress bars

## Documentation

- [Installation Guide](docs/INSTALL.md)
- [Usage Guide](docs/USAGE.md)
- [API Configuration](docs/API.md)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI | Cerebras (llama-3.1-8b) |
| Language | Python 3.9+ |
| Processing | Pandas |

## License

MIT License - See [LICENSE](LICENSE)

## Author

[abyanell24](https://github.com/abyanell24)

---

For detailed documentation, see the [docs/](docs/) folder.