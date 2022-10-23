from flask import Flask, render_template, request, session, redirect, url_for
from dbmanager import DB

app = Flask(__name__)
db = DB()


@app.route('/')
def index():
  if 'win' not in session:
    session['win'] = 'home'
  return render_template('index.html')  

@app.route('/home')
def home():
  session['win'] = 'home'
  return redirect(url_for('index'))

@app.route('/about')
def about():
  session['win'] = 'about'
  return redirect(url_for('index'))

@app.route('/profile')
def profile():
  if 'userdb' not in session:
    session['msg'] = 'Sign in First!'
    return redirect(url_for('index'))
  session['win'] = 'profile'
  return redirect(url_for('index'))

@app.route('/signin')
def signin():
  if 'userdb' in session:
    session['msg'] = 'You are already Signed in'
    return redirect(url_for('index'))
  if session['win'] !='signin':
    if session['win'] not in ('signin', 'signup'):
      session['tmp'] = session['win']
    session['win'] = 'signin'
    if 'form' in session:
      session.pop('form')
  return redirect(url_for('index'))

@app.route('/signup')
def signup():
  if 'userdb' in session:
    session['msg'] = 'You are already Signed in'
    return redirect(url_for('index'))
  if session['win'] !='signup':
    if session['win'] not in ('signin', 'signup'):
      session['tmp'] = session['win']
    session['win'] = 'signup'
    if 'form' in session:
      session.pop('form')
  
  return redirect(url_for('index'))

@app.route('/signout')
def signout():
  if 'userdb' not in session:
    session['msg'] = 'You are not signed in'
    return redirect(url_for('index'))
  session.pop('userdb')
  return redirect(url_for('index'))

@app.route('/handle_form', methods=['POST'])
def handle_form():
  if request.method == 'POST':
    
    if session['win'] == 'signin':
      session['form'] = {'username':request.form['username'],
                         'password':request.form['password']}
      if db.check_user(session['form']['username'], session['form']['password']):
        data = db.get_data(session['form']['username'])
        session['userdb'] = {'username':data['USERNAME'],
                             'firstname':data['FIRSTNAME'],
                             'lastname':data['LASTNAME'],
                             'email':data['EMAIL'],
                             'phone':data['PHONE']}
        session.pop('form')
        session['win'] = session['tmp']
        return redirect(url_for('index'))
      else:
        session['msg'] = 'Invalid username or password'
        return redirect(url_for('index'))
    
    elif session['win'] == 'signup':
      session['form'] = {'username':request.form['username'],
                         'password':request.form['password'],
                         'firstname':request.form['firstname'],
                         'lastname':request.form['lastname'],
                         'email':request.form['email'],
                         'phone':request.form['phone'],}
      if db.get_data(session['form']['username']) == None:
        db.add(session['form']['username'],
               session['form']['password'],
               session['form']['firstname'],
               session['form']['lastname'],
               session['form']['email'],
               session['form']['phone'],)
        data = db.get_data(session['form']['username'])
        session['userdb'] = {'username':data['USERNAME'],
                             'firstname':data['FIRSTNAME'],
                             'lastname':data['LASTNAME'],
                             'email':data['EMAIL'],
                             'phone':data['PHONE']}
        session.pop('form')
        session['win'] = session['tmp']
        return redirect(url_for('index'))
      else:
        session['msg'] = 'Username already exists'
        return redirect(url_for('index'))
    
    else:
      session['msg'] = 'Error with Form'
      return redirect(url_for('index'))

app.config['SECRET_KEY'] = '123456789'
app.run()