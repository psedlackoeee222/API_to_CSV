import pandas as pd

URL = "https://data.csu.gov.cz/api/dotaz/v1/data/vybery/CRUHVD1T2?format=CSV"
CSV_FILE = "csu_data.csv"

df = pd.read_csv(URL)
print(df.head())

df.to_csv(CSV_FILE, index=False, sep=";")
print(f"Uložené do {CSV_FILE}")