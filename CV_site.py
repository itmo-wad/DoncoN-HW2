from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'DoncoN_2_HW_DB'
app.config['MONGO_URL'] = 'mongodb://localhost:27017/DoncoN_2_HW_DB'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return "You are logged as " + session['username']
    return render_template('sign-in.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return 'Invalid username or password'



# @app.route('/')
# def index():
#     return redirect("/profile", code=302)

@app.route('/profile')
def profile():
    return render_template('CV_Nam.html')

if __name__ == '__main__':
    app.secret_key='secretkeyhere'
    app.run(host="localhost", port=5000, debug=True)
