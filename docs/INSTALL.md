# Installation Guide

This guide covers how to install and set up the AI CSV Cleaner application.

## Prerequisites

| Requirement | Version |
|-------------|----------|
| Python | 3.9 or higher |
| pip | Latest recommended |

## Option 1: pip (Recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/abyanell24/ai-csv-cleaner.git
cd ai-csv-cleaner
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Application

```bash
streamlit run app.py
```

### Step 5: Open Browser

Navigate to: `http://localhost:8501`

---

## Option 2: Conda

### Step 1: Create Environment

```bash
conda create -n ai-csv-cleaner python=3.11
conda activate ai-csv-cleaner
```

### Step 2: Clone and Install

```bash
git clone https://github.com/abyanell24/ai-csv-cleaner.git
cd ai-csv-cleaner
pip install -r requirements.txt
```

### Step 3: Run

```bash
streamlit run app.py
```

---

## Dependencies

The following packages are required:

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | >=1.28.0 | Web UI framework |
| pandas | >=2.0.0 | Data processing |
| cerebras | latest | AI inference client |
| cerebras-cloud-sdk | latest | Cerebras API SDK |

Install manually if needed:

```bash
pip install streamlit pandas cerebras
```

---

## Troubleshooting

### ModuleNotFoundError: No module named 'cerebras'

**Solution**: Reinstall cerebras in your environment:

```bash
pip install cerebras --force-reinstall
```

### Port 8501 already in use

**Solution**: Use a different port:

```bash
streamlit run app.py --server.port 8502
```

### Slow processing

**Solution**: For large CSV files, processing is done in batches. This is normal behavior.

---

## Next Steps

After installation, see [USAGE.md](./USAGE.md) for how to use the application.

For API key information, see [API.md](./API.md).