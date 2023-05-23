from flask import Flask, request, render_template, redirect, url_for, jsonify
import requests
from urllib import parse
import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client['sotube']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/sotube', methods=['GET', 'POST'])
def about():
    return render_template('sotube.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method=="POST":
        collection = db['user_info']
        email = request.form['email']
        passwd = request.form['password']
        collection.insert_one({'email' : email, 'password' : passwd})
        return redirect(url_for('home'))

@app.route('/contact', methods=['POST'])
def contact():
    if request.method=="POST":
        collection = db['contact']
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        collection.insert_one({'name' : name, 'email' : email, 'password' : message})
        return redirect(url_for('home'))

@app.route("/confirm_user", methods=['POST'])
def confirm_user():
    if request.method == "POST":
        collection = db['user_info']
        email = request.form.get('email')
        password = request.form.get('password')

        user = collection.find_one({'email' : email, 'password' : password})

        if user:
            return jsonify({'message' : 'Login succeed'}), 200
        else:
            return jsonify({'message' : 'Invalid email or Password'}), 401
        
@app.route("/email_check", methods=['POST'])
def email_check():
    if request.method == "POST":
        collection = db['user_info']
        email = request.json['email']
        user = collection.find_one({'email' : email})

        if user:
            return jsonify({'exists' : True})
        else:
            return jsonify({'exists' : False})

if __name__ == '__main__':
    app.run(port=5001, debug=True)