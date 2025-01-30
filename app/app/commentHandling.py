from flask import request, jsonify
from app import app, db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

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

    return jsonify({"message": "Comment added successfully", "success": True}), 201

@app.route('/api/comments/<int:article_id>', methods=['GET'])
def get_comments(article_id):
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.date_created.asc()).all()
    results = [{'id': comment.id, 'username': comment.username, 'text': comment.text, 'date_created': comment.date_created, 'likes': comment.likes, 'dislikes': comment.dislikes} for comment in comments]
    return jsonify(results)

@app.route('/api/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return jsonify({"message": "Comment liked successfully", "success": True}), 200

@app.route('/api/comments/<int:comment_id>/dislike', methods=['POST'])
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.dislikes += 1
    db.session.commit()
    return jsonify({"message": "Comment disliked successfully", "success": True}), 200