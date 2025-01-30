from flask import request
from flask_socketio import SocketIO, emit, join_room, leave_room
from app import app

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': f'{data["username"]} has joined the room.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'{data["username"]} has left the room.'}, room=room)

@socketio.on('comment')
def handle_comment(data):
    room = data['room']
    emit('comment', {'username': data['username'], 'text': data['text']}, room=room)