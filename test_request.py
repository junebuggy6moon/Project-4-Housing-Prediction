import requests

url = 'http://127.0.0.1:5000/geocode'
data = {'address': '1600 Amphitheatre Parkway, Mountain View, CA'}

response = requests.post(url, json=data)

print('Status Code:', response.status_code)
if response.status_code == 200:
    try:
        print('Response Body:', response.json())
    except ValueError:
        print('Response is not in JSON format:', response.text)
else:
    print('Failed to get a proper response:', response.text)
