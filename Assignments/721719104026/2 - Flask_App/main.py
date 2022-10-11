from flask import Flask, render_template, request, session, redirect, url_for
from userdata import DB

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
  if 'window' not in session:
    session['window'] = 'home'
  return render_template('index.html')


@app.route('/home')
def home():
  session['window'] = 'home'
  return redirect(url_for('index'))


@app.route('/about')
def about():
  session['window'] = 'about'
  return redirect(url_for('index'))


@app.route('/signin')
def signin():
  session['tmp'] = session['window']
  return render_template('signin.html', msg=None)


@app.route('/signup')
def signup():
  return render_template('signup.html', msg=None)


@app.route('/handle_form/<t>', methods=['POST'])
def handle_form(t):
  db = DB()
  if request.method == 'POST':
    
    if t == 'signin':
      if db.check_user(request.form['username'], request.form['password']):
        session['user'] = request.form['username']
        session['window'] = session['tmp']
        return redirect(url_for('index'))
        
      else:
        return render_template('signin.html', msg='Invalid username or password')
        
    elif t == 'signup':
      if db.check_username(request.form['username']):
        db.add(request.form['username'],
             request.form['firstname'],
             request.form['lastname'],
             request.form['email'],
             request.form['password'])
        session['user'] = request.form['username']
        session['window'] = session['tmp']
        return redirect(url_for('index'))
      else:
        return render_template('signup.html', msg='Username already exists')


@app.route('/signout')
def signout():
  session.pop('user')
  return redirect(url_for('index'))


app.config['SECRET_KEY'] = '123456789'
app.run(debug = True)  
