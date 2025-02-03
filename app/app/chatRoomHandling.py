from flask import request, jsonify
from app import app, db
from datetime import datetime

class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    if not ChatRoom.query.filter_by(name="Example Room 1").first():
        example_room1 = ChatRoom(name="Example Room 1")
        db.session.add(example_room1)
    if not ChatRoom.query.filter_by(name="Example Room 2").first():
        example_room2 = ChatRoom(name="Example Room 2")
        db.session.add(example_room2)
    db.session.commit()

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = ChatRoom.query.all()
    results = [{'id': room.id, 'name': room.name, 'date_created': room.date_created} for room in rooms]
    return jsonify(results)

@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"message": "Name is required", "success": False}), 400

    new_room = ChatRoom(name=name)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created successfully", "success": True}), 201


@app.route('/api/delete_room', methods=['POST'])
def delete_room():
    data = request.get_json()
    room_id = data.get('id')

    if not room_id:
        return jsonify({"message": "Room ID is required", "success": False}), 400

    room = ChatRoom.query.get(room_id)

    if not room:
        return jsonify({"message": "Room not found", "success": False}), 404

    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Room deleted successfully", "success": True}), 200




