import pandas as pd


def generate_csv_from_list(data: list, columns: list = None) -> bytes:
    """Generate CSV from list of dicts"""
    if not data:
        return b""
    
    df = pd.DataFrame(data, columns=columns)
    csv_string = df.to_csv(index=False)
    return csv_string.encode('utf-8')


def generate_csv_from_dict(data: dict, columns: list = None) -> bytes:
    if columns is None:
        columns = list(data.keys())
    df = pd.DataFrame([data], columns=columns)
    csv_string = df.to_csv(index=False)
    return csv_string.encode('utf-8')


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