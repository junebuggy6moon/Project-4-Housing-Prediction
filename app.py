from flask import Flask, request, jsonify, abort
from models import db, bcrypt, User
from dotenv import load_dotenv
import googlemaps
import os

load_dotenv() 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))


@app.route('/register', methods=['POST'])
def register():
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
    try:
        address = request.json.get('address')
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        return jsonify({'location': {'lat': 37.4221, 'lng': -122.0841}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
