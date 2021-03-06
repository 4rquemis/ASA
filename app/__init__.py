from flask import Flask
app = Flask(__name__)

from flask_assets import Environment 
assets = Environment(app)


from flaskext.mysql import MySQL
from config import ConfDb
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


from app import routes


