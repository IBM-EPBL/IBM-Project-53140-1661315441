from flask import Flask, render_template, request, session, redirect, url_for
from modules.dbmanager import DBManager
from modules.UserManagement import Profile, UserManagement

app = Flask(__name__)
HOSTNAME = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30376
SSLServerCertificate = 'DigiCertGlobalRootCA.crt'
UID = "szk22942"
PWD = "9tvjYOOk8eRYq5wu"

DB = DBManager(HOSTNAME, PORT, SSLServerCertificate, UID, PWD)
PR = Profile(DB)
UM = UserManagement(DB)
""" try: PR.signin('superadmin', 'toor1234') # TODO - Remove this line
except: DB.add_user('superadmin', 'toor1234', 'Super Admin', 'superadmin', '', '') """
try: PR.signin('dhinesh', 'helloworld') # TODO - Remove this line
except:
  DB.add_user('dhinesh', 'helloworld', 'Dhinesh', 'admin', 'dhinesh88825@gmail.com', '0987654321')
  PR.signin('dhinesh', 'helloworld')


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


# User Management - Pag
@app.route('/usermanagement')
def usermanagement():
  session['page'] = 'usermanagement'
  return render_template('usermanagement.html')

@app.route('/usermanagement/<a>', methods=['GET', 'POST'])
def usermanagement_action(a):
  if a == 'adduser':
    pass

  elif a == 'removeuser':
    pass

  else:
    return render_template('404.html')


# Profile - Page
@app.route('/profile')
def profile():
  session['page'] = 'profile'
  return render_template('profile.html', mode='view')

@app.route('/profile/<a>', methods=['POST', 'GET'])
def profile_action(a):
  if a == 'edit':
    return render_template('profile.html', mode='edit')

  elif a == 'confirm':
    try:
      PR.update(request.form['name'], request.form['role'],
                      request.form['email'], request.form['phone'])
      return redirect(url_for('profile'))
    except Exception as e:
      session['msg'] = str(e)
      return render_template('profile.html', mode='edit')

  elif a == 'discard':
    return redirect(url_for('profile'))

  elif a == 'changepassword':
    return render_template('profile.html', mode='changepassword')

  elif a == 'changepasswordconfirm':
    try:
      password, npassword = request.form['password'], request.form['npassword']
      PR.update_password(password, npassword)
      session['msg'] = 'Password Changed Successfully'
    except Exception as e:
      session['msg'] = str(e)
    return redirect(url_for('profile'))

  elif a == 'signout':
    try:
      PR.signout()
    except Exception as e:
      session['msg'] = str(e)
    return redirect(url_for('signin'))
  
  elif a == 'removeuser':
    try:
      password = request.form['password']
      PR.remove_user(password)
      session['msg'] = 'User removed successfully'
    except Exception as e:
      session['msg'] = str(e)
      return redirect(url_for('profile'))
    return redirect(url_for('signin'))
    
  else:
    return render_template('404.html')


# Sign In - Page
@app.route('/signin')
def signin():
  if PR.user:
    session['msg'] = 'You are already Signed in'
    return redirect(url_for(session['page']))
  if 'form' in session:
    session.pop('form')
  return render_template('signin.html')

@app.route('/signin/handle_form', methods=['POST'])
def signin_action():
  session['form'] = {'username': request.form['username'],
                       'password': request.form['password']}
  try:
    PR.signin(session['form']['username'], session['form']['password'])
    session['msg'] = 'Signed in successfully'
    session['page'] = session['tmp']
  except Exception as e:
    session['msg'] = str(e)
    return redirect(url_for(session['page']))
  session.pop('form')
  return redirect(url_for(session['page']))




@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.context_processor
def inject_data():
  return dict(PR=PR, UM=UM)


if __name__ == '__main__':
  app.config['SECRET_KEY'] = '123456789'
  app.run(debug=True)
