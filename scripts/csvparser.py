# parse csv using pandas
import pandas as pd
import os


def parse_csv(file_path):
    """
    Parse a CSV file and return a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The parsed DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error parsing the CSV file: {e}")
