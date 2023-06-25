from flask import Flask, render_template, jsonify
import mysql.connector
import time
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE')
)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_data', methods=['GET'])
def update_data():
    while True:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.commit()
        return jsonify(users=users)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
