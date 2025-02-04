from flask import request, jsonify
from app import app, db
from datetime import datetime
import paho.mqtt.publish as publish


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False) 
    author = db.Column(db.String(100), nullable=False)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  

with app.app_context():
    db.create_all()

@app.route('/api/search', methods=['GET'])
def search_articles():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    author = request.args.get('author', '')
    date = request.args.get('date', '')

    articles_query = Article.query.filter(Article.title.contains(query))

    if category:
        articles_query = articles_query.filter(Article.category.contains(category))
    
    if author:
        articles_query = articles_query.filter(Article.author.contains(author))
    
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        articles_query = articles_query.filter(Article.date_created >= date_obj)

    articles = articles_query.all()

    results = [{
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'category': article.category,
        'author': article.author,
        'date_created': article.date_created.isoformat() 
    } for article in articles]
    
    return jsonify(results)


@app.route('/api/create', methods=['POST'])
def create_article():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    category = data.get('category', 'general')
    author = data.get('author')

    if not title or not content or not author:
        return jsonify({"message": "Title, content and author are required", "success": False}), 400

    new_article = Article(title=title, content=content, category=category, author=author)
    db.session.add(new_article)
    db.session.commit()

    publish.single(f'projektProtokoly/notifications/{category}', f'New article in {category}: {title}', hostname='broker.hivemq.com')

    return jsonify({"message": "Article created successfully", "success": True}), 201

@app.route('/api/articles/<category>', methods=['GET'])
def get_articles_by_category(category):
    query = request.args.get('query', '')
    articles = Article.query.filter(Article.category == category, Article.title.contains(query)).all()
    results = [{'id': article.id, 'title': article.title, 'content': article.content, 'author': article.author, 'date_created': article.date_created} for article in articles]
    return jsonify(results)

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article_by_id(article_id):
    article = Article.query.get(article_id)
    if article:
        result = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'category': article.category,
            'author': article.author,
            'date_created': article.date_created
        }
        return jsonify(result), 200
    else:
        return jsonify({"message": "Article not found"}), 404
    

@app.route('/api/articles/<username>', methods=['GET'])
def get_articles_by_user(username):
    articles = Article.query.filter_by(author=username).all()
    results = [{'id': article.id, 'title': article.title, 'content': article.content, 'category': article.category, 'author': article.author, 'date_created': article.date_created} for article in articles]
    return jsonify(results)

#zrob tu do debugu fetch autors plis


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    data = request.get_json()
    article = Article.query.get(article_id)
    if article:
        article.title = data.get('title', article.title)
        article.content = data.get('content', article.content)
        article.category = data.get('category', article.category)
        article.author = data.get('author', article.author)
        db.session.commit()
        return jsonify({"message": "Article updated successfully"}), 200
    else:
        return jsonify({"message": "Article not found"}), 404
    

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = Article.query.get(article_id)
    if article:
        db.session.delete(article)
        db.session.commit()
        return jsonify({"message": "Article deleted successfully", "success": True}), 200
    else:
        return jsonify({"message": "Article not found", "success": False}), 404
    


@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Article.query.order_by(Article.date_created.desc())
    
    result = [{
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'category': article.category,
        'author': article.author,
        'date_created': article.date_created.isoformat() 
    } for article in articles]

    return jsonify(result)

    
