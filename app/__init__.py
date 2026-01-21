from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for sessions

# MySQL configuration
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

from app import routes
