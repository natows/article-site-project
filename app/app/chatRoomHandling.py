from flask import request, jsonify
from app import app, db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableList




class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    subscribers = db.Column(MutableList.as_mutable(JSON), default=list)


    

with app.app_context():
    db.create_all()
    if not ChatRoom.query.filter_by(name="General").first():
        example_room1 = ChatRoom(name="General")
        db.session.add(example_room1)
    if not ChatRoom.query.filter_by(name="Whats up?").first():
        example_room2 = ChatRoom(name="Whats up?")
        db.session.add(example_room2)
    db.session.commit()

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = ChatRoom.query.all()
    results = [{'id': room.id, 'name': room.name, 'date_created': room.date_created, 'subscribers': room.subscribers} for room in rooms]
    return jsonify(results)

@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"message": "Name is required", "success": False}), 400
    
    existing_room = ChatRoom.query.filter_by(name=name).first()
    if existing_room:
        return jsonify({"message": "Room with this name already exists", "success": False}), 400

    new_room = ChatRoom(name=name)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created successfully", "success": True}), 201


@app.route('/api/delete_room/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = ChatRoom.query.get(room_id)

    if not room:
        return jsonify({"message": "Room not found", "success": False}), 404

    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Room deleted successfully", "success": True}), 200

@app.route('/api/update_room/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room = ChatRoom.query.get(room_id)

    if not room:
        return jsonify({"message": "Room not found", "success": False}), 404

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"message": "Name is required", "success": False}), 400

    room.name = name
    db.session.commit()

    return jsonify({"message": "Room updated successfully", "success": True}), 200


