from flask import Flask, render_template, request, session, redirect, url_for
from modules.dbmanager import DBManager
from modules.UserManagement import UserManagement

app = Flask(__name__)
HOSTNAME = "21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
PORT = 31864
SSLServerCertificate = 'DigiCertGlobalRootCA.crt'
UID = "wxq10827"
PWD = "ymVaT0kPM3W5j0g5"
UM = UserManagement(DBManager(HOSTNAME, PORT, SSLServerCertificate, UID, PWD))

# Root URL
@app.route('/')
def index():
  return redirect(url_for('dashboard'))

# Dashboard - Page
@app.route('/dashboard')
def dashboard():
  session['page'] = 'dashboard'
  return render_template('dashboard.html')

# Store - Page
@app.route('/store')
def store():
  session['page'] = 'store'
  return render_template('store.html')

# Warehouse - Page
@app.route('/warehouse')
def warehouse():
  session['page'] = 'warehouse'
  return render_template('warehouse.html')

# User Management - Page
@app.route('/usermanagement')
def usermanagement():
  session['page'] = 'usermanagement'
  return render_template('usermanagement.html')

# Profile - Page
@app.route('/profile')
def profile():
  if not UM.user:
    session['msg'] = 'Sign in First!'
    return redirect(url_for(session['page']))
  session['page'] = 'profile'
  return render_template('profile.html')

# Sign In - Page
@app.route('/signin')
def signin():
  if UM.user:
    session['msg'] = 'You are already Signed in'
    return redirect(url_for(session['page']))
  if session['page'] !='signin':
    if 'form' in session:
      session.pop('form')
    session['tmp'] = session['page']
    session['page'] = 'signin'
  return render_template('signin.html')

@app.route('/signin/handle_form', methods=['POST'])
def signin_form():
  session['form'] = {'username':request.form['username'],
                     'password':request.form['password']}
  try:
    UM.signin(session['form']['username'], session['form']['password'])
    session['msg'] = 'Signed in successfully'
    session['page'] = session['tmp']
  except Exception as e:
    session['msg'] = str(e)
    return redirect(url_for(session['page']))
  session.pop('form')
  return redirect(url_for(session['page']))

# Sign Out
@app.route('/signout')
def signout():
  try:
    UM.signout()
    session['msg'] = 'Signed out successfully'
  except Exception: session['msg'] = Exception
  return redirect(url_for(session['page']))


# Remove User
@app.route('/removeuser')
def removeuser():
  try:
    UM.remove_user()
    session['msg'] = 'User removed successfully'
  except Exception: session['msg'] = Exception
  return redirect(url_for(session['page']))


app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.context_processor
def inject_data():
  return dict(UM=UM)


if __name__ == '__main__':
  app.config['SECRET_KEY'] = '123456789'
  app.run(debug=True)
