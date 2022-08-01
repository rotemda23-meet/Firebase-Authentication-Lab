from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
config= {"apiKey": "AIzaSyB29sOtmoLJlQAsaun0ntE8xKKwW2Dwz_8",
  "authDomain": "rotem-and-more.firebaseapp.com",
  "projectId": "rotem-and-more",
  "storageBucket": "rotem-and-more.appspot.com",
  "messagingSenderId": "457525107556",
  "appId": "1:457525107556:web:cafbe24bf75099dab97871",
  "measurementId": "G-BEHV39NH3Q"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()



@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=='GET':
        return render_template('home.html')
    else:
        password=request.form["password"]
        email=request.form["email"]
        try:
            login_session['user'] = auth.sign_in_user_with_password_and_email(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
        return render_template('home.html')
    else:
        password=request.form["password"]
        email=request.form["email"]
        try:
            login_session['user'] = auth.create_user_with_password_and_email(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)