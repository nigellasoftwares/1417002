# main.py
import threading
import webview
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask


# Create a Flask app instance
app = Flask(__name__)

app.config['MYSQL_HOST'] = '159.223.32.228'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nigella@123'
app.config['MYSQL_DB'] = 'nigella_form'

mysql = MySQL(app)



@app.route("/")
def hello():
    # mysql data
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Fetch data from the users table
    cursor.execute("SELECT * FROM users")
    usersF = cursor.fetchall()
    print('User data: ', usersF)

    return f"<h3> Database- {usersF} </h3>"

# Start Flask server in a separate thread
def run_flask():
    app.run(host="127.0.0.1", port=5000)

# Create a WebView window
def create_webview():
    webview.create_window("My App", "http://127.0.0.1:5000")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    create_webview()

    webview.start()
