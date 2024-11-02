from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

# root
@app.route('/')
def hello():
    return '<h1>Hello!! Welcome to my Watchlist!</h1><img s<img src="https://media.tenor.com/s3I_IAym7_EAAAAj/rick-and-morty.gif">'

# /index page
@app.route('/index')
def index():
    return 'This is index page'

# /home page
@app.route('/home')
def home():
    return 'This is home page'

# /user/<name> page
# using escape from markupsafe
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)} page'


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='AngusAu'))
    print(url_for('user_page', name='NettieWong'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'