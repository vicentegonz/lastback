import requests
import csv

API_KEY = '9yydziuU.WptcL4vglt0VHmyJngoKiZlN8Qz5ZLQZ'
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
      print(f'Column names are {", ".join(row)}')
    else:
      lines+=1
      params = {
        "name": row[0],
        "value": float(row[1]),
        "store": int(row[2]),
        "units": row[3],
        "category": row[4],
        "date": row[5],
      }
      response = requests.put(url, data=params, headers=headers,)
      if response.status_code == 201 or response.status_code == 200 :
        continue
      else:
        res = response.json()
        print(res)
        break
  print(f'Processed {lines-1} KPIs')








