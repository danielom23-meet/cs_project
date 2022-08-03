from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase



config = {
  "apiKey": "AIzaSyA_cycsH9cx7SonxowXgfzUa9mfr0rSzuA",
  "authDomain": "project-firebase-66130.firebaseapp.com",
  "projectId": "project-firebase-66130",
  "storageBucket": "project-firebase-66130.appspot.com",
  "messagingSenderId": "1090676868452",
  "appId": "1:1090676868452:web:9f3af260c9a25616d6e671",
  "measurementId": "G-XKQ6HTJW4V",
  "databaseURL": "https://project-firebase-66130-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('home'))
        except:
            error = "Error with signing up"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = {"email": request.form['email'],"password": request.form['password'],"full_name": request.form['full_name'],"username": request.form['username']}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('home'))
        except:
            error = "Error with signing up"
    return render_template("signup.html", error = error)

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/home')
def home():
    return render_template("testProject.html")

@app.route('/store', methods = ['GET', 'POST'])
def store():
    error = ""
    if request.method == 'POST':
        product = {"quantity": 10, "price": 100}
        try:
            db.child("Users").child(login_session['user']['localId']).child("cart").push(product)
            return redirect(url_for('cart'))
        except:
            error = "adding failed"
    return render_template("store.html")

@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    return render_template("cart.html", cart = db.child("Users").child(login_session['user']['localId']).child("cart").get().val())


if __name__ == '__main__':
    app.run(debug=True)