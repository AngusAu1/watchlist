import os
import sys
import click

from flask import Flask
from markupsafe import escape
#from flask import url_for
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, url_for, redirect, flash

WIN = sys.platform.startswith('win')
if WIN:                                                                                     # if it is windows, using ///
    prefix = 'sqlite:///'
else:                                                                                       # otherwise, using ////
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')     # sqlite:/// absolute address for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                        # disable the tracing of modifications 

db = SQLAlchemy(app)

class User(db.Model):                                                                       # Table name: user
    id = db.Column(db.Integer, primary_key=True)                                            # Primary Key
    name = db.Column(db.String(20))                                                         # user name


class Movie(db.Model):                                                                      # table name: movie
    id = db.Column(db.Integer, primary_key=True)                                            # Primary Key
    title = db.Column(db.String(60))                                                        # Movie title
    year = db.Column(db.String(4))                                                          # Movie year

@app.cli.command()                                                                          # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')                            # setup the option
def initdb(drop):
    """Initialize the database."""
    if drop:                                                                                # check is ti input the option
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')                                                     # echo the message

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# name = 'Angus Au'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]

@app.context_processor
def inject_user():  
    user = User.query.first()
    return dict(user=user)                                  # return to dict, it's equal to: return {'user':user}


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(404)                                      # pass the error code that need to be handle
def page_not_found(e):                                      # accept the exception as a parameter
    return render_template('404.html', user=user), 404      # returned to template

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# root
@app.route('/', methods=['GET', 'POST'])
#def hello():
#    return '<h1>Hello!! Welcome to my Watchlist!</h1><img s<img src="https://media.tenor.com/s3I_IAym7_EAAAAj/rick-and-morty.gif">'

def index():
    if request.method == 'POST':                             # Check if it is POST request method
        # get the table data
        title = request.form.get('title')                    
        year = request.form.get('year')
        # verify data
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')                         # return error message 'Invalid input'
            return redirect(url_for('index'))               # Redirect to the root main page
        # store the date that submitted
        movie = Movie(title=title, year=year)               
        db.session.add(movie)                               # add the data into table: movie
        db.session.commit()                                 # commit
        flash('Item created.')                              # dispaly 'Item created'
        return redirect(url_for('index'))                   # Redirect to the root main page
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)     # pass the data to the index.html

# Edit Movie page
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':                                    # Check if it is POST request method
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))     # Redirect to the Edit Movie page

        movie.title = title                                         # Update title
        movie.year = year                                           # Update year
        db.session.commit()                                         # commit
        flash('Item updated.')
        return redirect(url_for('index'))                           # Redirect to main page

    return render_template('edit.html', movie=movie)                # pass the data to the edit.html

# Delete Movie record
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])        # Only allow POST request method
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)                        # get the Movie record
    db.session.delete(movie)                                        # delete the movie record
    db.session.commit()                                             # commit
    flash('Item deleted.')
    return redirect(url_for('index'))                               # redirect to main page

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