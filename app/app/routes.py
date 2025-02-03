from app import app
from flask import render_template
from app.articleHandling import Article
from app.commentHandling import Comment

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signin')
def signin_page():
    return render_template('signin.html')
@app.route('/account')
def account_page():
    return render_template('account.html')

@app.route('/create_article')
def create_article_page():
    return render_template('create.html')

@app.route('/sport')
def sport_page():
    return render_template('sport.html')

@app.route('/technology')
def technology_page():
    return render_template('technology.html')

@app.route('/health')
def health_page():
    return render_template('health.html')

@app.route('/entertainment')
def entertainment_page():
    return render_template('entertainment.html')



@app.route('/modify/<int:article_id>')
def modify_article(article_id):
    return render_template('modify.html', article_id=article_id)



@app.route('/article/<int:article_id>')
def article_page(article_id):
    article = Article.query.get_or_404(article_id)
    comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.date_created.asc()).all()
    return render_template('article.html', article=article, comments=comments)


@app.route('/room/<room_name>')
def room_page(room_name):
    return render_template('room.html', room_name=room_name)

