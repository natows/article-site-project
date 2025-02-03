from flask import request, jsonify, Blueprint
from app import app, db
from datetime import datetime
import jwt
import json

comment_bp = Blueprint('comment', __name__)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    user_likes = db.Column(db.Text, default='[]') 

    def get_user_likes(self):
        return json.loads(self.user_likes)

    def set_user_likes(self, user_likes):
        self.user_likes = json.dumps(user_likes)

with app.app_context():
    db.create_all()

@app.route('/api/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    article_id = data.get('article_id')
    username = data.get('username')
    text = data.get('text')

    if not article_id or not username or not text:
        return jsonify({"message": "All fields are required", "success": False}), 400

    new_comment = Comment(article_id=article_id, username=username, text=text)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({
        "message": "Comment added successfully",
        "success": True,
        "id": new_comment.id,
        "article_id": new_comment.article_id,
        "username": new_comment.username,
        "text": new_comment.text,
        "date_created": new_comment.date_created,
        "likes": new_comment.likes,
        "dislikes": new_comment.dislikes,
        "user_likes": new_comment.get_user_likes()
    }), 201

@app.route('/api/comments/<int:article_id>', methods=['GET'])
def get_comments(article_id):
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.date_created.asc()).all()
    results = [{'id': comment.id, 'username': comment.username, 'text': comment.text, 'date_created': comment.date_created, 'likes': comment.likes, 'dislikes': comment.dislikes, 'user_likes': comment.get_user_likes()} for comment in comments]
    return jsonify(results)

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully", "success": True}), 200

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    data = request.get_json()
    comment = Comment.query.get_or_404(comment_id)
    comment.text = data.get('text', comment.text)
    db.session.commit()
    return jsonify({"message": "Comment updated successfully", "success": True}), 200

@app.route('/api/comments/<int:comment_id>/like', methods=['PATCH'])
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing", "success": False}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['user']
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired", "success": False}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token", "success": False}), 401

    user_likes = comment.get_user_likes()
    if username not in user_likes:
        user_likes.append(username)
        comment.set_user_likes(user_likes)
        comment.likes += 1
        db.session.commit()

    return jsonify(success=True, likes=comment.likes, users=comment.get_user_likes())

@app.route('/api/comments/<int:comment_id>/unlike', methods=['DELETE'])
def unlike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Token is missing", "success": False}), 401

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['user']
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired", "success": False}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token", "success": False}), 401

    user_likes = comment.get_user_likes()
    if username in user_likes:
        user_likes.remove(username)
        comment.set_user_likes(user_likes)
        comment.likes -= 1
        db.session.commit()

    return jsonify(success=True, likes=comment.likes, users=comment.get_user_likes())

app.register_blueprint(comment_bp, url_prefix='/api')
