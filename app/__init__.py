from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

TOKEN_SECRET = '$ecret'

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = "$ecretey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zxfinuecvtacov:8884337627fe8b7643e415260903ca8d792d81c54033c32e4666268066ed9c55@ec2-54-243-213-188.compute-1.amazonaws.com:5432/dfu6bnq0a1b8fl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"


db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
token_key = app.config['TOKEN_SECRET']
from app import views

