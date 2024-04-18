import requests

url = 'http://127.0.0.1:5000/predict'

data = {
    "MedInc": 3.8716,
    "HouseAge": 21,
    "AveRooms": 4.875,
    "AveBedrms": 1.006,
    "Population": 322,
    "AveOccup": 2.555,
    "Latitude": 37.54,
    "Longitude": -122.29
}

response = requests.post(url, json=data)

print(f"Prediction: {response.text}")
