import requests
import csv

API_KEY = 'ROTci9Go.VKjLkVI31KNj4q0lELQ9pC591VMr39fq'
file_name = 'service-indicators.csv'

headers = {
  'X-API-KEY': f"{API_KEY}"
}

url = 'http://localhost:8000/v1/operations/service-indicators/'

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
        "amount_of_surveys": int(row[3]),
        "nps": int(row[4]) if int(row[5]) else 0,
        "amount_nps": int(row[5]),
        "experience": int(row[6]) if int(row[7]) else 0,
        "amount_experience": int(row[7]),
        "kindness": int(row[8]) if int(row[9]) else 0,
        "amount_kindness": int(row[9]),
        "waiting_time": int(row[10]) if int(row[11]) else 0,
        "amount_waiting_time": int(row[11]),
        "speed": int(row[12]) if int(row[13]) else 0,
        "amount_speed": int(row[13]),
        "quality": int(row[14]) if int(row[15]) else 0,
        "amount_quality": int(row[15]),
        "bathroom": int(row[16]) if int(row[17]) else 0,
        "amount_bathroom": int(row[17]),
      }
      response = requests.put(url, data=params, headers=headers)
      if response.status_code == 201 or response.status_code == 200 :
        continue
      else:
        print("Some Error")
        #res = response.json()
        print(response)
        break
  print(f'Processed {lines-1} Service Indicators')









