from flask import Flask, render_template, jsonify
import mysql.connector
import time
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)
load_dotenv()

app.config['APP_NAME'] = 'WIREPASS'
app.config['APP_VERSION'] = '1.0'

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
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.commit()
    return jsonify(users=users)

@app.after_request
def add_app_info_to_header(response):
    response.headers['X-Application-Name'] = app.config['APP_NAME']
    response.headers['X-Application-Version'] = app.config['APP_VERSION']
    return response

@app.context_processor
def inject_app_info():
    return dict(app_name=app.config['APP_NAME'], app_version=app.config['APP_VERSION'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
