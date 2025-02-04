from flask import request, Response
from flask_socketio import SocketIO, emit, join_room, leave_room
from app import app,db
from app.messageHandling import Message
import time, json
from app.sseHandler import notify_subscribers
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
    username = data['username']
    join_room(room)
    print(f'{username} has joined the room {room}.')
  
    emit('message', {'username': 'System', 'text': f'{username} has joined the room.'}, room=room)


@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f'{data["username"]} has left the room'}, room=room)

@socketio.on('comment')
def handle_comment(data):
    room = data['room']
    emit('comment', {'id':data['id'],'username': data['username'], 'text': data['text'], 'likes': 0, 'user_likes': data['user_likes']}, room=room)

@socketio.on('delete_comment')
def handle_delete_comment(data):
    room = data['room']
    emit('delete_comment', {'id': data['id']}, room=room)

@socketio.on('edit_comment')
def handle_edit_comment(data):
    room = data['room']
    emit('edit_comment', {'id': data['id'], 'text': data['text']}, room=room)

@socketio.on('like_comment')
def handle_like_comment(data):
    room = data['room']
    emit('like_comment', {'id': data['id'], 'likes': data['likes']}, room=room)

@socketio.on('unlike_comment')
def handle_unlike_comment(data):
    room = data['room']
    emit('unlike_comment', {'id': data['id'], 'likes': data['likes']}, room=room)


@socketio.on('message')
def handle_message(data):
    room = data['room']
    username = data['username']
    text = data['text']

    new_message = Message(username=username, text=text, room=room)
    db.session.add(new_message)
    db.session.commit()

    emit('message', {
        'username': username, 
        'text': text, 
        'id': new_message.id 
    }, room=room)

    notify_subscribers(room, {"message": text})



@socketio.on('delete_message')
def handle_delete_message(data):
    room = data['room']
    message_id = data['message_id']

    message = Message.query.filter_by(id=message_id).first()
    if message:
        db.session.delete(message) 
        db.session.commit()

    
        emit('delete_message', {'message_id': message_id}, room=room)

@socketio.on('edit_message')
def handle_edit_messade(data):
    room = data['room']
    message_id = data['message_id']
    new_text = data['text']

    message = Message.query.filter_by(id=message_id).first()
    if message:
        message.text = new_text
        db.session.commit()

        emit('edit_message', {'message_id': message_id, 'text': new_text}, room=room)




