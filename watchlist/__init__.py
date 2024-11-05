import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:                                     # If it is Windows, use ///                                                # if it is windows, using ///
    prefix = 'sqlite:///'
else:                                       # Otherwise, use ////                                                   # otherwise, using ////
    prefix = 'sqlite:////'


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'dev'

'''
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
'''

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
#app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'watchlist/data.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        return dict(user=current_user)  # return to the current user
    return dict(user=None)  # else, which mean have not login yet, and return None

from watchlist import views, errors, commands