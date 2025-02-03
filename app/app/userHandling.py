from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from app import app, db
import jwt
import datetime
import bcrypt
import json


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    subscriptions = db.Column(db.Text, nullable=True, default='[]') 

def create_admin_users():
    admin_users = [
        {"username": "admin1", "password": "admin1password"},
        {"username": "admin2", "password": "admin2password"},
        {"username": "Igor Kałabun", "password": "KotekPiesek2137"}
    ]

    for admin in admin_users:
        existing_user = User.query.filter_by(username=admin["username"]).first()
        if not existing_user:
            hashed_password = bcrypt.hashpw(admin["password"].encode('utf-8'), bcrypt.gensalt())
            new_admin = User(username=admin["username"], password=hashed_password.decode('utf-8'), is_admin=True)
            db.session.add(new_admin)
            db.session.commit()

with app.app_context():
    db.create_all()
    create_admin_users()


@app.route('/api/data', methods=['GET'])
def get_data():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    try:
        token = token.split()[1]  
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403

    data = {
        "name": "Flask Backend",
        "version": "1.0"
    }
    return jsonify(data)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        response = make_response(jsonify({"message": "Login successful", "success": True}), 200)
        response.set_cookie('token', token, httponly=True, secure=True)
        return response
    else:
        return jsonify({"message": "Invalid credentials", "success": False}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "User logged out!"}), 200)
    response.set_cookie('token', '', expires=0)
    return response

@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists", "success": False}), 409
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    response = make_response(jsonify({"message": "Rejestracja zakończona sukcesem", "success": True}), 201)
    response.set_cookie('token', token, httponly=True, secure=True)
    return response

@app.route('/api/user', methods=['GET'])
def get_user():
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(username=username).first()
        return jsonify({"id": user.id, "username": username, "is_admin": user.is_admin, "subscriptions": user.subscriptions}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403
    
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "password": user.password, "is_admin": user.is_admin} for user in users]
    return jsonify(users_list)

@app.route('/api/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        new_username = data.get('username')
        new_password = data.get('password')
        new_status = data.get('is_admin')

        if new_username:
            user.username = new_username
        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password.decode('utf-8')
        if new_status:
            user.is_admin = new_status

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403

@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully", "success": True}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(username=username).first()

        channel = request.json.get('channel')
        if not channel:
            return jsonify({"message": "Channel is missing!"}), 400

        subscriptions = json.loads(user.subscriptions)
        if channel not in subscriptions:
            subscriptions.append(channel)
            user.subscriptions = json.dumps(subscriptions)
            db.session.commit()
        return jsonify({"message": f"Subscribed to {channel}", "subscriptions": subscriptions})
    except Exception as e:
        return jsonify({"message": f"Token is invalid! {str(e)}"}), 403

@app.route('/api/unsubscribe', methods=['DELETE'])
def unsubscribe():
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(username=username).first()

        channel = request.json.get('channel')
        if not channel:
            return jsonify({"message": "Channel is missing!"}), 400

        subscriptions = json.loads(user.subscriptions)
        if channel in subscriptions:
            subscriptions.remove(channel)
            user.subscriptions = json.dumps(subscriptions)
            db.session.commit()
        return jsonify({"message": f"Unsubscribed from {channel}", "subscriptions": subscriptions})
    except Exception as e:
        return jsonify({"message": f"Token is invalid! {str(e)}"}), 403
    
@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing!"}), 403
    
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        subscriptions = json.loads(user.subscriptions)
        return jsonify({"subscriptions": subscriptions}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403





