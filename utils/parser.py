import pandas as pd
import json
import io


def parse_csv_to_dict(file) -> dict:
    df = pd.read_csv(file)
    return df.to_dict(orient='records')


def parse_csv_to_json(file, indent: int = 2) -> str:
    df = pd.read_csv(file)
    return df.to_json(orient='records', indent=indent)


def parse_csv_to_list(file) -> list:
    file.seek(0)
    df = pd.read_csv(file)
    return df.to_dict(orient='records')


def get_csv_info(file) -> dict:
    df = pd.read_csv(file)
    return {
        "columns": list(df.columns),
        "row_count": len(df),
        "dtypes": df.dtypes.apply(str).to_dict()
    }