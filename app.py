from flask import Flask, request, jsonify, abort
from models import db, bcrypt, User
from dotenv import load_dotenv
import pickle
import pandas as pd
import googlemaps
import os

from geocode import geocode_address
from geocode import get_latitude_from_geocoded_address
from geocode import get_longitude_from_geocoded_address

load_dotenv() 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))


@app.route('/', methods=['GET'])
def homepage():
    return "<h1>Home Page</h1>"


@app.route('/register', methods=['POST'])
def register():
    """A route to register users"""
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first() is not None:
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({'message': 'Email already exists'}), 400
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/geocode', methods=['POST'])
def geocode():
    """A route to get the geocoded data of an address"""
    try:
        address_json = request.json.get('address')

        if not address_json:
            return jsonify({'error': 'Address is required'}), 400
        
        geocode_result= geocode_address(gmaps, address_json)

        if not geocode_result:
            return jsonify({'error': 'Geocoded result could not be acquired'}),400
        
        return jsonify(geocode_result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        median_income=request.json.get("MedInc")
        house_age=request.json.get("HouseAge")
        average_rooms=request.json.get("AveRooms")
        average_bedrooms=request.json.get("AveBedrms")
        population=request.json.get("Population")
        average_occupancy=request.json.get("AveOccup")
        address=request.json.get("address")
    
        geocode_result= geocode_address(gmaps, address)
        latitude=get_latitude_from_geocoded_address(geocode_data=geocode_result)
        longitude=get_longitude_from_geocoded_address(geocode_data=geocode_result)

        data_dictionary= {
            "MedInc": median_income,
            "HouseAge": house_age,
            "AveRooms": average_rooms,
            "AveBedrms": average_bedrooms,
            "Population": population,
            "AveOccup": average_occupancy,
            "Latitude":latitude,
            "Longitude":longitude
            }
        
        prediction_data_df=pd.DataFrame(data_dictionary, index=[0])

        model_file = open("rf_model.pkl",'rb')
        random_forest_model = pickle.load(model_file)
        prediction=random_forest_model.predict(prediction_data_df)
        print(f"Prediction:{prediction}")

        return jsonify(prediction.tolist()[0]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
