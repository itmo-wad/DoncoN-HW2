from flask import Flask, render_template, redirect, url_for, request, session
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'DoncoN_2_HW_DB'
app.config['MONGO_URI'] = 'mongodb://192.168.0.178:27017/DoncoN_2_HW_DB'

mongo = PyMongo(app)

def is_logged():
    return 'username' in session

@app.route('/')
def index():
    if is_logged():
        return redirect(url_for('profile'))
    return render_template('log-in.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if request.form['pass'].encode('utf-8') == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return "Invalid username or password"


@app.route('/profile')
def profile():
    if not is_logged():
        return redirect(url_for('login'))
    return render_template('CV_Nam.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = "secretkeyhere"
    app.run(host="localhost", port=5000, debug=True)
