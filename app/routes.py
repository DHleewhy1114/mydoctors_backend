from app import app
from app import login_manager
from models import User

@app.route('/')
def index():
    return "hello"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login')
def login():
    return "login"

"""
@app.route('/register')

"""