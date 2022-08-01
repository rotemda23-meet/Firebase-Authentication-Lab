from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



config= {"apiKey": "AIzaSyB29sOtmoLJlQAsaun0ntE8xKKwW2Dwz_8",
  "authDomain": "rotem-and-more.firebaseapp.com",
  "projectId": "rotem-and-more",
  "storageBucket": "rotem-and-more.appspot.com",
  "messagingSenderId": "457525107556",
  "appId": "1:457525107556:web:cafbe24bf75099dab97871",
  "measurementId": "G-BEHV39NH3Q",
  "databaseURL": "https://omg-yes-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ''
    if request.method=='POST':
        password = request.form['password']    
        email = request.form['email']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = 'fail'
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        password=request.form['password']    
        email=request.form['email']
        full_name = request.form['full_name']
        bio = request.form['bio']
        username = request.form['username']
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {"username":username, "full_name":full_name, "bio": bio}
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('add_tweet'))

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=='POST':
        title = request.form["title"]
        text = request.form["text"]
        tweet = {"title":title, "text":text, "uid": login_session['user']['localId']}
        try:
            db.child("Tweets").push(tweet)
            return redirect(url_for("all_tweets"))
        except:
            return render_template("add_tweet.html", errormsg = "could not add tweet")
    else:
        return render_template("add_tweet.html")



@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweet = db.child("Tweets").get().val()
    return render_template("tweets.html", tweet=tweet)



if __name__ == '__main__':
    app.run(debug=True)
