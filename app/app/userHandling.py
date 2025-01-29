from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app, db
import jwt
import datetime
import bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()


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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials", "success": False}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({"message": "User logged out!"})

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
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"message": "Rejestracja zakończona sukcesem", "token": token, "success": True}), 201

@app.route('/api/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        return jsonify({"username": username}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "password": user.password} for user in users]
    return jsonify(users_list)

@app.route('/api/update_user', methods=['PUT'])
def update_user():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        new_username = data.get('username')
        new_password = data.get('password')

        if new_username:
            user.username = new_username
        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password.decode('utf-8')

        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403

@app.route('/api/delete_user', methods=['DELETE'])
def delete_user():
    token = request.headers.get('Authorization').split()[1]
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        username = decoded_token['user']
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully", "success": True}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid!"}), 403


