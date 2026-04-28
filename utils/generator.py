import pandas as pd
import io


def generate_csv_from_list(data: list, columns: list = None) -> bytes:
    df = pd.DataFrame(data, columns=columns)
    # Convert all columns to string to avoid dtype issues
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df.to_csv(index=False).encode('utf-8')


def generate_csv_from_dict(data: dict, columns: list = None) -> bytes:
    if columns is None:
        columns = list(data.keys())
    df = pd.DataFrame([data], columns=columns)
    return df.to_csv(index=False).encode('utf-8')


def generate_csv_file(data: list, filename: str = "output.csv") -> str:
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([data])
    df.to_csv(filename, index=False)
    return filename


def list_to_csv_string(data: list, columns: list = None) -> str:
    df = pd.DataFrame(data, columns=columns)
    return df.to_csv(index=False)