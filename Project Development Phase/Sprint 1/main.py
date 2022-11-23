from flask import Flask, render_template, request, session, redirect, url_for
from modules.DBManager import DBManager
from modules.DBManagerProxy import DBManagerProxy
from modules.UserManagement import UserManagement

app = Flask(__name__)
HOSTNAME = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30376
UID = "szk22942"
PWD = "YhVluZhcmvFKS8NT"

DB = DBManagerProxy(HOSTNAME, PORT, UID, PWD)
UM = UserManagement(DB)


# Session Variables:
# page - The page the user is currently on
# message - The message to display to the user
# username - The username of the user



if not UM.check_username('superadmin'):
  UM.add_user('superadmin', 'toor1234', 'Super Admin', 'superadmin', '', '')

if not UM.check_username('dhinesh'):
  UM.add_user('dhinesh', 'helloworld', 'Dhinesh', 'admin', 'dhinesh88825@gmail.com', '0987654321')


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
  return render_template('usermanagement.html', mode='view')

@app.route('/usermanagement/<a>', methods=['GET', 'POST'])
def usermanagement_action(a):
  if a == 'adduser':
    return render_template('usermanagement.html', mode='add')
  
  elif a == 'adduser2':
    username, password = request.form['username'], request.form['password']
    if UM.check_username(username):
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
      name, email, phone = request.form['name'], request.form['email'], request.form['phone']
      UM.edit_user(username=session['username'], newname=name, newemail=email, newphone=phone)
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
      if not UM.check_user(session['username'], password):
        session['message'] = 'Password Incorrect'
        return render_template('profile.html', mode='changepassword')
      UM.change_password(session['username'], newpassword)
      session['message'] = 'Password Changed Successfully'
    except Exception as e:
      session['message'] = str(e)
    return redirect(url_for('profile'))

  elif a == 'signout':
    try:
      session.pop('username', None)
      session['message'] = 'Signed Out Successfully'
    except Exception as e:
      session['message'] = str(e)
    return redirect(url_for('signin'))
  
  elif a == 'removeuser':
    try:
      password = request.form['password']
      if not UM.check_user(session['username'], password):
        print(-3)
        session['message'] = 'Password Incorrect'
        return render_template('profile.html', mode='view')
      print(-4)
      UM.remove_user(session['username'])
      session.pop('username', None)
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
  if 'user' in session:
    session['message'] = 'You are already Signed in'
    return redirect(url_for(session['page']))
  return render_template('signin.html')

@app.route('/signin/handle_form', methods=['POST'])
def signin_action():
  username, password = request.form['username'], request.form['password']
  if UM.check_user(username, password):
    session['username'] = username
  else:
    session['message'] = 'Invalid Username or Password'
    return redirect(url_for('signin'))
  return redirect(url_for(session['page']))



@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.context_processor
def inject_data():
  return dict(UM=UM)



if __name__ == '__main__':
  app.config['SECRET_KEY'] = '123456789'
  app.run(debug=True)
