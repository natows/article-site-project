
from datetime import datetime
from app import app, db

from flask import jsonify


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    room = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/api/messages/<room>', methods=['GET'])
def get_messages(room):
    messages = Message.query.filter_by(room=room).order_by(Message.timestamp).all()
    return jsonify([{'username': msg.username, 'text': msg.text, 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages])

#edit message i delete message (delete dostepne dla admina wszystko a dla uzytkownika tylko ich wiadomosci)
