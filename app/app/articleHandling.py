from flask import request, jsonify
from app import app, db
from datetime import datetime
import paho.mqtt.publish as publish


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  

with app.app_context():
    db.create_all()

@app.route('/api/search', methods=['GET'])
def search_articles():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    articles = Article.query.filter(Article.title.contains(query), Article.category.contains(category)).all()
    results = [{'id': article.id, 'title': article.title, 'content': article.content, 'category': article.category, 'date_created': article.date_created} for article in articles]
    return jsonify(results)

@app.route('/api/create', methods=['POST'])
def create_article():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    category = data.get('category', 'general')

    if not title or not content:
        return jsonify({"message": "Title and content are required", "success": False}), 400

    new_article = Article(title=title, content=content, category=category)
    db.session.add(new_article)
    db.session.commit()

    publish.single(f'projektProtokoly/notifications/{category}', f'New article in {category}: {title}', hostname='broker.hivemq.com')

    return jsonify({"message": "Article created successfully", "success": True}), 201

@app.route('/api/articles/<category>', methods=['GET'])
def get_articles_by_category(category):
    query = request.args.get('query', '')
    articles = Article.query.filter(Article.category == category, Article.title.contains(query)).all()
    results = [{'id': article.id, 'title': article.title, 'content': article.content, 'date_created': article.date_created} for article in articles]
    return jsonify(results)