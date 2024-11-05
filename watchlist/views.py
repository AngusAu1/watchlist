from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie

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

'''
@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='AngusAu'))
    print(url_for('user_page', name='NettieWong'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'
'''