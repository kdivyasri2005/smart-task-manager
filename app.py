from flask import Flask, render_template
from flask_login import LoginManager, login_required

from db import db
from extensions import socketio

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:root@localhost/taskmanager'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ INITIALIZE DATABASE
db.init_app(app)

# ✅ INITIALIZE SOCKETIO
socketio.init_app(
    app,
    cors_allowed_origins="*"
)

# ✅ LOGIN MANAGER
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'auth.login'

from models.models import User, Task


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(User, int(user_id))


@app.route('/')
def home():

    return "Smart Task Manager Backend Running"


@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')


# ✅ CREATE DATABASE TABLES
with app.app_context():

    db.create_all()


# ✅ REGISTER BLUEPRINTS
from routes.auth import auth
app.register_blueprint(auth)

from routes.task import task
app.register_blueprint(task)


# ✅ RUN APP
if __name__ == '__main__':

    socketio.run(
        app,
        debug=True,
        allow_unsafe_werkzeug=True
    )