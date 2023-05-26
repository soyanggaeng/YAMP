from flask import Blueprint, session, redirect, url_for, jsonify, request
from pymongo import MongoClient
from config import *
from functools import wraps
import datetime

client = MongoClient(MONGODB_HOST)

db = client[MONGODB_DATABASE]

bp = Blueprint("fun_blueprint", __name__);

#decorater
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login_status' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#login / logout
@bp.route("/logout")
@login_required
def logout():
    session.pop('login_status', None)
    return redirect(url_for('home'))

@bp.route("/login_status")
def login_status():
    return jsonify({'login_status' : session.get("login_status", False)})


@bp.route('/add_user', methods=['POST'])
def add_user():
    if request.method=="POST":
        collection = db['user_info']
        email = request.form['email']
        passwd = request.form['password']
        registered =datetime.datetime.utcnow()
        collection.insert_one({'email' : email, 'password' : passwd, 'registered' : registered})
        return redirect(url_for('login'))
    
@bp.route('/update_user', methods=['POST'])
@login_required
def update_user():
    if request.method=="POST":
        collection = db['user_info']
        user_filter = {'email' : session.get("email")}
        collection.update_one(user_filter, {"$set" : request.json})
        user = collection.find_one(user_filter, {'_id': False})
        return jsonify(user)

@bp.route('/get_user', methods=['POST'])
@login_required
def get_user():
    if request.method=="POST":
        collection = db['user_info']
        user_filter = {'email' : session.get("email")}
        user = collection.find_one(user_filter, {'_id': False})
        return jsonify(user)


@bp.route('/contact', methods=['POST'])
def contact():
    if request.method=="POST":
        collection = db['contact']
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        collection.insert_one({'name' : name, 'email' : email, 'password' : message})
        return redirect(url_for('home'))

        
@bp.route("/email_check", methods=['POST'])
def email_check():
    if request.method == "POST":
        collection = db['user_info']
        email = request.json['email']
        user = collection.find_one({'email' : email})

        if user:
            return jsonify({'exists' : True})
        else:
            return jsonify({'exists' : False})
        
@bp.route("/confirm_user", methods=['POST'])
def confirm_user():
    if request.method == "POST":
        collection = db['user_info']
        email = request.form.get('email')
        password = request.form.get('password')
        user = collection.find_one({'email' : email, 'password' : password})

        if user:
            session['login_status'] = True
            session['email'] = email
            return jsonify({'message' : 'Login succeed'}), 200
        else:
            return jsonify({'message' : 'Invalid email or Password'}), 401


@bp.route('/getFeedback', methods=['POST'])
def get_feedback():
    if request.method=="POST":
        collection = db['feedback']
        youtuber = request.form['youtuber']
        voucher_usage = request.form['voucher-usage']
        satisfaction_rating = request.form['satisfaction-rating']
        service_improvements = request.form['service-improvements']
        youtuber_satisfaction = request.form['youtuber-satisfaction']
        youtuber_feedback = request.form['youtuber-feedback']
        
        dict_fb = {
            'youtuber' : youtuber,
            'voucher-usage' : voucher_usage,
            'satisfaction-rating' : satisfaction_rating,
            'service-improvements' : service_improvements,
            'youtuber-satisfaction' : youtuber_satisfaction,
            'youtuber-feedback' : youtuber_feedback
        }

        collection.insert_one(dict_fb)
        return redirect(url_for('home'))