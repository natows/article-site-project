from app import app
from flask import render_template

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
