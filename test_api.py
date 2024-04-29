import requests

url = 'http://127.0.0.1:5000/predict'

data = {
    "MedInc": 3.8716,
    "HouseAge": 21,
    "AveRooms": 4.875,
    "AveBedrms": 1.006,
    "Population": 322,
    "AveOccup": 2.555,
    "address":"1600 Amphitheatre Parkway, Mountain View, CA"
}

response = requests.post(url, json=data)

print(f"Prediction: {response.text}")
