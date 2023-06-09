from flask import Flask, request, render_template, redirect, url_for, jsonify, session, g
import json
# from pymongo import MongoClient
from config import *
from db_setup import get_db

app = Flask(__name__)

from func import bp, login_required
from recommend import bp2

app.register_blueprint(bp)
app.register_blueprint(bp2)

app.config.from_pyfile('config.py')

secret_key = app.config.get('SECRET_KEY', 'default_secret')

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def teardown_db(exc):
    db = g.pop('db', None)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', login_status = session.get('login_status', False))

@app.route('/sotube', methods=['GET', 'POST'])
def about():
    return render_template('sotube.html', login_status = session.get('login_status', False))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(session.get('login_status', False)):
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(session.get('login_status', False)):
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/mypage', methods=['GET', 'POST'])
@login_required
def mypage():
    return render_template('mypage.html')

@app.route('/feedback', methods=['GET', 'POST'])
@app.route('/feedback/<service>')
@login_required
def feedback(service=None):
    return render_template('feedback.html')

@app.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    return render_template('overview.html')

@app.route('/proposal', methods=['GET', 'POST'])
@login_required
def proposal():
    return render_template('proposal.html')

@app.route('/keyword', methods=['GET', 'POST'])
@login_required
def keyword():
    return render_template('keyword.html')



if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5001)
    app.run(port=5001)