import requests
import csv

API_KEY = 'zijPNWEZ.NXTmpGDg7DuD3vlHCgYAfpf4Uvn1IyyR'
file_name = 'kpis.csv'

headers = {
  'X-API-KEY': f"{API_KEY}"
}

url = 'http://localhost:8000/v1/operations/kpis/'

with open(file_name) as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=';')
  lines = 0
  for row in csv_reader:
    if lines== 0:
      lines+=1
      #print(f'Column names are {", ".join(row)}')
    else:
      lines+=1
      params = {
        "date": row[0],
        "store": int(row[1]),
        "category": row[3],
        "net_sale": int(row[4]),
        "contribution": int(row[5]),
        "transactions": int(row[6]),
        "gross_sale": int(row[7]),
      }
      response = requests.put(url, data=params, headers=headers,)
      if response.status_code == 201 or response.status_code == 200 :
        continue
      else:
        res = response.json()
        print(res)
        break
  print(f'Processed {lines-1} KPIs')








