PARSER_SYSTEM_PROMPT = """You are a CSV data analyst. Analyze and describe CSV data provided by the user. Be generic - handle any type of CSV data (sales, inventory, population, employees, customers, products, etc)."""


PARSER_USER_PROMPT = """Analyze this CSV data and provide a summary in JSON format:
{data}

Provide a JSON response with:
- "summary": Brief description of what this data is about
- "columns": List of columns with their data types
- "row_count": Number of rows in the data
- "data_quality": Any issues found (missing values, duplicates, invalid data)"""



GENERATOR_SYSTEM_PROMPT = """You are a CSV data generator. Your task is to convert user input into properly formatted CSV data."""


GENERATOR_USER_PROMPT = """Based on the following input, generate CSV data:
{input_data}

Generate valid CSV data in the following format:
- Use proper column headers
- Data should be comma-separated
- Output raw CSV string only, no explanation"""



TRANSFORM_SYSTEM_PROMPT = """You are a CSV data transformer. Your task is to modify or convert CSV data based on user instructions."""


TRANSFORM_USER_PROMPT = """Transform this CSV data based on the instruction:
{instruction}

Original CSV data:
{csv_data}

Output the result in JSON format with key "data" containing the transformed data as a list of objects."""


CLEANER_SYSTEM_PROMPT = """You are an industrial-grade CSV data cleaning assistant.
You MUST apply PROPER data cleaning rules to ALL CSV data regardless of content type (sales, inventory, population, employees, etc).

Your role is to:
1. Remove duplicate rows
2. Fix all data types (numbers, dates, strings, booleans)
3. Handle all missing/invalid values
4. Standardize formats
5. Validate data consistency

CRITICAL RULES:
- Always output valid JSON (array of objects)
- Never leave invalid values like "abd", "abc", "N/A", "four hundred" in number fields
- Always convert dates to YYYY-MM-DD format
- Always lowercase categorical fields
- Always trim whitespace"""


CLEANER_USER_PROMPT = """Clean this CSV data dengan INDUSTRY STANDARD rules.

STANDARD DATA CLEANING RULES:

1. MISSING VALUES (Semua Field):
   - Number fields: isi dengan 0 atau nilai median
   - Text required: isi dengan "Unknown"
   - Text optional: biarkan sebagai empty string ""
   - Date fields: isi dengan null atau tanggal default

2. DATA TYPE FIXING (Semua Records):
   - Hapus symbols dari numbers: $, %,(), Letters dari numeric fields
   - Konversi text ke number: "abc"→0, "four hundred"→400, "300$"→300
   - Fix dates ke format YYYY-MM-DD
   - Boolean fields: true/false, yes/no → 1/0

3. DUPLICATE REMOVAL:
   - Hapus baris yang 100% identik
   - Keep first occurrence

4. DATA VALIDATION:
   - Fix negative numbers yang tidak masuk akal (quantity=-2 → 2)
   - Invalid numbers: "abd", "abc", "N/A" → 0
   - Fix calculated fields if possible
   - Flag outliers (>3 std deviasi) tapi jangan hapus

5. TEXT STANDARDIZATION:
   - Lowercase untuk categorical fields (kategori, status, type, dll)
   - Trim semua whitespace (leading/trailing)
   - Remove extra spaces
   - Standardize: empty string, null, "NA", "N/A" → ""

6. FORMAT STANDARDIZATION:
   - Numbers: max 2 decimal places
   - Currency: numeric tanpa symbol
   - Phone: numeric only
   - Email: lowercase

INPUT DATA (JSON format):
{data}

OUTPUT: Return ONLY cleaned data dalam JSON format yang sama seperti input. No explanation, no markdown, no code blocks. JSON array of objects only."""