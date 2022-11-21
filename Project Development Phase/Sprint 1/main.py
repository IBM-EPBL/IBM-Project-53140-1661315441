from flask import Flask, render_template, request, session, redirect, url_for
from modules.DBManager import DBManager
from modules.UserManagement import Profile, UserManagement

app = Flask(__name__)
HOSTNAME = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30376
SSLServerCertificate = 'DigiCertGlobalRootCA.crt'
UID = "szk22942"
PWD = "9tvjYOOk8eRYq5wu"

DB = DBManager(HOSTNAME, PORT, SSLServerCertificate, UID, PWD)
PR = Profile(DB)
UM = UserManagement(DB, 'superadmin', 'toor1234')
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
  return render_template('usermanagement.html', mode='view')

@app.route('/usermanagement/<a>', methods=['GET', 'POST'])
def usermanagement_action(a):
  print('User Management: ' + a)
  if a == 'adduser':
    return render_template('usermanagement.html', mode='add')
  
  elif a == 'adduser2':
    username = request.form['username']
    password = request.form['password']
    print('User Management: ' + a + ' - ' + username + ' - ' + password)
    if DB.check_username(username):
      session['message'] = 'Username Already exists'
      return render_template('usermanagement.html', mode='add')
    return render_template('usermanagement.html', mode='add2', username=username, password=password)
  
  elif a == 'confirmadduser':
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    role = request.form['role']
    email = request.form['email']
    phone = request.form['phone']
    print('User Management: ' + a + ' - ' + username + ' - ' + password + ' - ' + name + ' - ' + role + ' - ' + email + ' - ' + phone)
    try:
      UM.add_user(username, password, name, role, email, phone)
      session['message'] = 'User Added Successfully'
      return redirect(url_for('usermanagement'))
    except Exception as e:
      session['message'] = str(e)
    return render_template('usermanagement.html', mode='add')
  
  elif a == 'discardadduser':
    return redirect(url_for('usermanagement'))
  
  elif a == 'edituser':
    username = request.form['username']
    try:
      user = UM.get_user(username)
      return render_template('usermanagement.html', mode='edit', username=user.USERNAME, 
                             password=user.PASSWORD, name=user.name, role=user.role, 
                             email=user.email, phone=user.phone)
    except Exception as e:
      session['message'] = str(e)
    return redirect(url_for('usermanagement'))

  elif a == 'removeuser':
    username = request.form['username']
    return redirect(url_for('usermanagement'))

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

  elif a == 'confirmedit':
    try:
      PR.update(request.form['name'], request.form['email'], request.form['phone'])
      return redirect(url_for('profile'))
    except Exception as e:
      session['message'] = str(e)
    return render_template('profile.html', mode='edit')

  elif a == 'discardedit':
    return redirect(url_for('profile'))

  elif a == 'changepassword':
    return render_template('profile.html', mode='changepassword')

  elif a == 'changepasswordconfirm':
    try:
      password, newpassword = request.form['password'], request.form['newpassword']
      PR.update_password(password, newpassword)
      session['message'] = 'Password Changed Successfully'
    except Exception as e:
      session['message'] = str(e)
    return redirect(url_for('profile'))

  elif a == 'signout':
    try:
      PR.signout()
      UM.pull(PR)
      session['message'] = 'Signed out Successfully'
    except Exception as e:
      session['message'] = str(e)
    return redirect(url_for('signin'))
  
  elif a == 'removeuser':
    try:
      password = request.form['password']
      PR.remove_user(password)
      session['message'] = 'User Removed Successfully'
    except Exception as e:
      session['message'] = str(e)
      return redirect(url_for('profile'))
    return redirect(url_for('signin'))
    
  else:
    return render_template('404.html')


# Sign In - Page
@app.route('/signin')
def signin():
  if PR.user:
    session['message'] = 'You are already Signed in'
    return redirect(url_for(session['page']))
  return render_template('signin.html')

@app.route('/signin/handle_form', methods=['POST'])
def signin_action():
  try:
    username, password = request.form['username'], request.form['password']
    PR.signin(username, password)
    UM.pull(PR)
    session['message'] = 'Signed in Successfully'
  except Exception as e:
    session['message'] = str(e)
    return redirect(url_for('signin'))
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
