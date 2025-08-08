import requests
import pandas as pd

download_url = "http://34.30.192.111:3000/export-csv"

response = requests.get(download_url)
filename = 'latest_data.csv'
with open(filename, 'wb') as f:
    f.write(response.content)

df = pd.read_csv(filename)
print(df.head())