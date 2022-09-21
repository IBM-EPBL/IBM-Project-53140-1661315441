from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/')
def index():
  session['user'] = None
  return render_template('home.html')


@app.route('/home')
def home():
  print("Session User:", session['user'])
  return render_template('home.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/signin')
def signin():
  return render_template('signin.html')


@app.route('/signup')
def signup():
  return render_template('signup.html')


@app.route('/submitSignIn', methods=['POST'])
def submitSignIn():
  session['user'] = request.form['username']
  return render_template('home.html')


@app.route('/submitSignUp', methods=['POST'])
def submitSignUp():
  session['user'] = request.form['username']
  return render_template('home.html')


@app.route('/signout')
def signOut():
  session['user'] = None
  return render_template('home.html')
app.config['SECRET_KEY'] = '123456789'
app.run()