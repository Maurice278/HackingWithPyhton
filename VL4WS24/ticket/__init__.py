from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER440710_mo:Test2468?!@maurice278.lima-db.de/db_440710_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='sdfsdfsdfsdfsdf'

db = SQLAlchemy(app)

from ticket import routes