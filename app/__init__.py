from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "$ecretey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://oiayogvmthyxhc:b4950779f81c42c9f733990c7c0959abfd2e53ba2cae09b14f4fcda6c9e3004a@ec2-54-163-246-193.compute-1.amazonaws.com:5432/djgjcjfpp13un'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"

db = SQLAlchemy(app)


app.config.from_object(__name__)
from app import views
