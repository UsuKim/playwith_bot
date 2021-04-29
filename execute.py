import requests

url = 'https://api.qwer.pw/request/hangang_temp'

params = {'apikey': 'guest'}

res = requests.get(url, params=params)

temp = res.json()[1]['respond']['temp']

print(temp)