from flask import Blueprint, Response, request, jsonify
import json
from app import db
from app.userHandling import User
import queue



sse = Blueprint('sse', __name__)




subscribers = {}

def notify_subscribers(room_name, message):
    if room_name in subscribers:
        for subscriber in subscribers[room_name]:
            subscriber.put(message)


def event_stream(room_name):
    def generate():
        q = queue.Queue()
        if room_name not in subscribers:
            subscribers[room_name] = []
        subscribers[room_name].append(q)
        try:
            while True:
                result = q.get()
                yield f"data: {json.dumps(result)}\n\n"
        except GeneratorExit:
            subscribers[room_name].remove(q)

    return Response(generate(), content_type='text/event-stream')


@sse.route('/sse/subscribe/<room_name>', methods=['POST'])
def subscribe(room_name):
    data = request.get_json()
    username = data.get('user')
    
    if not username:
        return jsonify({"message": "Username is required", "success": False}), 400

    q = queue.Queue()
    
    if room_name not in subscribers:
        subscribers[room_name] = []
    
    subscribers[room_name].append(q)

    user = User.query.filter_by(username=username).first()
    if user:
        if room_name not in user.subscribed_rooms:
            user.subscribed_rooms.append(room_name)
            db.session.commit()


    return jsonify({"message": f"Subscribed {username} to {room_name}", "success": True}), 200


@sse.route('/sse/subscribe/<room_name>', methods=['GET'])
def get_messages(room_name):
    return event_stream(room_name)

@sse.route('/sse/send_message/<room_name>', methods=['POST'])
def send_message(room_name):
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"message": "Message is required", "success": False}), 400

    notify_subscribers(room_name, {"message": message})
    return jsonify({"message": "Message sent to subscribers", "success": True}), 200
