from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import Flask, render_template

app = Flask(__name__)

name = 'Angus Au'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

# root
@app.route('/')
#def hello():
#    return '<h1>Hello!! Welcome to my Watchlist!</h1><img s<img src="https://media.tenor.com/s3I_IAym7_EAAAAj/rick-and-morty.gif">'

def index():
    return render_template('index.html', name=name, movies=movies)

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