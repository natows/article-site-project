from flask import request, jsonify, Blueprint
from app import app, db
from datetime import datetime
import jwt


comment_bp = Blueprint('comment', __name__)

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

    return jsonify({
        "message": "Comment added successfully",
        "success": True,
        "id": new_comment.id,
        "article_id": new_comment.article_id,
        "username": new_comment.username,
        "text": new_comment.text,
        "date_created": new_comment.date_created
    }), 201

@app.route('/api/comments/<int:article_id>', methods=['GET'])
def get_comments(article_id):
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.date_created.asc()).all()
    results = [{'id': comment.id, 'username': comment.username, 'text': comment.text, 'date_created': comment.date_created, 'likes': comment.likes, 'dislikes': comment.dislikes} for comment in comments]
    return jsonify(results)

# @comment_bp.route('/comments/<int:comment_id>/like', methods=['POST'])
# def like_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     comment.likes += 1
#     db.session.commit()
#     return jsonify(success=True, likes=comment.likes)

# @comment_bp.route('/comments/<int:comment_id>/dislike', methods=['POST'])
# def dislike_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     comment.dislikes += 1
#     db.session.commit()
#     return jsonify(success=True, dislikes=comment.dislikes)

# @comment_bp.route('/comments/<int:comment_id>/unlike', methods=['POST'])
# def unlike_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     if comment.likes > 0:
#         comment.likes -= 1
#     db.session.commit()
#     return jsonify(success=True, likes=comment.likes)

# @comment_bp.route('/comments/<int:comment_id>/undislike', methods=['POST'])
# def undislike_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     if comment.dislikes > 0:
#         comment.dislikes -= 1
#     db.session.commit()
#     return jsonify(success=True, dislikes=comment.dislikes)


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


@comment_bp.route('api/comments/<int:comment_id>/like', methods=['PATCH'])
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return jsonify(success=True, likes=comment.likes)

@comment_bp.route('/comments/<int:comment_id>/dislike', methods=['PATCH'])
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.dislikes += 1
    db.session.commit()
    return jsonify(success=True, dislikes=comment.dislikes)

@comment_bp.route('/comments/<int:comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.likes > 0:
        comment.likes -= 1
    db.session.commit()
    return jsonify(success=True, likes=comment.likes)

@comment_bp.route('/comments/<int:comment_id>/dislike', methods=['DELETE'])
def undislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.dislikes > 0:
        comment.dislikes -= 1
    db.session.commit()
    return jsonify(success=True, dislikes=comment.dislikes)


app.register_blueprint(comment_bp, url_prefix='/api')
