import os
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('env.cfg')
app.secret_key = os.urandom(12)

import mongo


def get_mongo_connection():
    try:
        conn = mongo.MongoDB(host=app.config['MYSQL_HOST'],port=app.config['MYSQL_PORT'],db=app.config['MONGO_DB'])
        return conn
    except Exception as e:
        print(e)
        

@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        
        res = get_mongo_connection().check_user(session['username'],session['password'])
 
        if res:
            return render_template('dashboard.html', user=session['username'])
        else:
            return render_template('index.html', error = "Invalid Username or Password")
    except Exception as e:
        print(e)
        

@app.route('/users', methods=['GET', 'POST'])
def users():
    try:
        if session['username'] is not None:
            res = get_mongo_connection().check_user(session['username'],session['password'])
            users = get_mongo_connection().get_users()
            print(users)
        if users:
            return render_template('users.html', users= users)
        else:
            return render_template('index.html', error = "Invalid Username or Password")
    except Exception as e:
        print(e)


@app.route('/')
def index():
    return render_template("index.html")


    
if __name__ == "__main__":
    app.run(debug=True, host=app.config['FLASK_HOST'], port=app.config['FLASK_PORT'], threaded=True)