import os
import sys
import click

from flask import Flask
from markupsafe import escape
#from flask import url_for
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required, logout_user
from flask_login import login_required, current_user

WIN = sys.platform.startswith('win')
if WIN:                                                                                     # if it is windows, using ///
    prefix = 'sqlite:///'
else:                                                                                       # otherwise, using ////
    prefix = 'sqlite:////'

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dev'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')     # sqlite:/// absolute address for the database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                        # disable the tracing of modifications 


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'watchlist/data.db'))
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)

# class User(db.Model):                                                                       # Table name: user
#     id = db.Column(db.Integer, primary_key=True)                                            # Primary Key
#     name = db.Column(db.String(20))                                                         # user name
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))                                                     # username
    password_hash = db.Column(db.String(128))                                               # password hash

    def set_password(self, password):                                                       # set_password method, password is a parameter here
        self.password_hash = generate_password_hash(password)                               # 

    def validate_password(self, password):                                                  # validate password method, password is a parameter here
        return check_password_hash(self.password_hash, password)                            # return a bool

class Movie(db.Model):                                                                      # table name: movie
    id = db.Column(db.Integer, primary_key=True)                                            # Primary Key
    title = db.Column(db.String(60))                                                        # Movie title
    year = db.Column(db.String(4))                                                          # Movie year
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                               # New add user id
    


# Initialize Flask-login
login_manager = LoginManager(app) 
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))                                                     # Use ID as User model's PK to query user account
    return user                                                                             # Return to user



@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)                                                         # set password
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)                                                         # set password
        db.session.add(user)

    db.session.commit()                                                                     # commit
    click.echo('Done.')


@app.cli.command()                                                                          # declare as a command, pass the name parameter to self-define command
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
    #user = User.query.first()
    #return dict(user=user)                                  # return to dict, it's equal to: return {'user':user}
    if current_user.is_authenticated:
        return dict(user=current_user)  # return to the current user
    return dict(user=None)  # else, which mean have not login yet, and return None

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
        if not current_user.is_authenticated:                # If the current user is not authenticated yet,...
            return redirect(url_for('index'))                # then redirect to main page
        # get the table data
        title = request.form.get('title')                    
        year = request.form.get('year')
        # verify data
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')                         # return error message 'Invalid input'
            return redirect(url_for('index'))               # Redirect to the root main page
        # store the date that submitted
        #movie = Movie(title=title, year=year)   
        movie = Movie(title=title, year=year, user_id=current_user.id)            
        db.session.add(movie)                               # add the data into table: movie
        db.session.commit()                                 # commit
        flash('Item created.')                              # dispaly 'Item created'
        return redirect(url_for('index'))                   # Redirect to the root main page
    #movies = Movie.query.all()

    if current_user.is_authenticated:
        movies = Movie.query.filter_by(user_id=current_user.id).all()
    else:
        movies =[]

    return render_template('index.html', movies=movies)     # pass the data to the index.html

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        #user = User.query.first()
        user = User.query.filter_by(username=username).first()
        # Verify user name and password
        #if username == user.username and user.validate_password(password):
        if user and user.validate_password(password):
            login_user(user)                                # Login
            flash('Login success.')
            return redirect(url_for('index'))               # redirect to root main page 

        flash('Invalid username or password.')              # Display error message if verify failed
        return redirect(url_for('login'))                   # redirect to login page

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()                                           # Logout user
    flash('Goodbye.')
    return redirect(url_for('index'))                       # redirect to root main page

# Setting for user account
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

# Create_user
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']

        # Validate the input
        if not username or not name or not password:
            flash('Incorrect input, please complete all fields')
            return redirect(url_for('create_user'))

        # check user account existing or not
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('The user name already existed. Please select another user name.')
            return redirect(url_for('create_user'))

        # create new user
        new_user = User(username=username, name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Create user account successfully!')
        return redirect(url_for('login'))

    return render_template('create_user.html')


# Edit Movie page
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
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