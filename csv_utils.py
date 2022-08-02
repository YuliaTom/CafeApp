import csv
import pandas as pd


def read_file(file_name) -> list[dict]:
    try:
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            result = [row for row in reader]
            return result
    except IOError:
        return []


def write_to_csv(file_name, dict_list):
    with open(file_name, "w") as file:
        w = csv.DictWriter(file, dict_list[0].keys())
        w.writeheader()
        for dict in dict_list:
            w.writerow(dict)


def csv_headers(file_name: str) -> list:
    df = scv_to_df(file_name)
    columns = list(df.columns)
    return columns


def scv_to_df(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name)
    return (df)


def print_csv_file(file_name: str):
    df = scv_to_df(file_name)
    df.index = df.index + 1
    print(df)
