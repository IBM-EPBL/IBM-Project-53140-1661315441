from flask import Flask, render_template, request, session, redirect, url_for
from modules.DBManager import DBManager
from modules.DBManagerProxy import DBManagerProxy
from modules.UserManagement import UserManagement
from modules.FacilityManagement import FacilityManagement
from modules.StockManagement import StockManagement

app = Flask(__name__)
HOSTNAME = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30376
UID = "szk22942"
PWD = "YhVluZhcmvFKS8NT"

DB = DBManagerProxy(HOSTNAME, PORT, UID, PWD)
UM = UserManagement(DB)
FM = FacilityManagement(DB)
SM = StockManagement(DB)


# Session Variables:
# page - The page the user is currently on
# message - The message to display to the user
# username - The username of the user



# Root URL
@app.route('/')
def index():
  return redirect(url_for('dashboard'))


# Dashboard - Page
@app.route('/dashboard')
def dashboard():
  session['page'] = 'dashboard'
  return render_template('dashboard.html')



# Stock - Page
# stock - id, name, type, price, quantity, facility
@app.route('/stock')
def stock():
  session['page'] = 'stock'
  return render_template('stock.html', mode='view')

@app.route('/stock/<a>', methods=['GET', 'POST'])
def stock_mode(a):
  if a == 'add':
    return render_template('stock.html', mode='add')
  elif a == 'update':
    id = request.form['id']
    quantity = request.form['quantity']
    SM.edit_quantity(id, quantity)
    return render_template('stock.html', mode='view')
  elif a == 'edit':
    id = request.form['id']
    return render_template('stock.html', mode='edit', id=id)
  elif a == 'delete':
    id = request.form['id']
    return render_template('stock.html', mode='delete', id=id)
  else:
    return render_template('404.html')

@app.route('/stock/<a>/<b>', methods=['GET', 'POST'])
def stock_action(a, b):
  if b == 'discard':
    return redirect(url_for('stock'))
  elif b == 'save':
    if a == 'add':
      name = request.form['name']
      type = request.form['type']
      price = request.form['price']
      quantity = request.form['quantity']
      facility = request.form['facility']
      SM.add_item(name, type, price, quantity, facility)
      return redirect(url_for('stock'))
    elif a == 'edit':
      id = request.form['id']
      name = request.form['name']
      type = request.form['type']
      price = request.form['price']
      quantity = request.form['quantity']
      facility = request.form['facility']
      SM.edit_item(id, name, type, price, quantity, facility)
      return redirect(url_for('stock'))
    elif a == 'delete':
      id = request.form['id']
      SM.remove_item(id)
      return redirect(url_for('stock'))
    else:
      return render_template('404.html')
  else:
    return render_template('404.html')




# Facilities - Page
# facility - id(auto), name(50), type(20), address(255), email(320), phone(15)
@app.route('/facilities')
def facilities():
  session['page'] = 'facilities'
  return render_template('facilities.html', mode='view')
# Modes: view, add, edit, delete
@app.route('/facilities/<a>', methods=['GET', 'POST'])
def facilities_mode(a):
  if a == 'add':
    return render_template('facilities.html', mode='add')
  elif a == 'edit':
    id = request.form['id']
    print('\n\n\n')
    print('id:',id)
    return render_template('facilities.html', mode='edit', id=id)
  elif a == 'delete':
    id = request.form['id']
    return render_template('facilities.html', mode='delete', id=id)
  else:
    return render_template('404.html')

@app.route('/facilities/<a>/<b>', methods=['GET', 'POST'])
def facilities_action(a,b):
  if b == 'discard':
    return redirect(url_for('facilities'))
  elif b == 'save':
    if a == 'add':
      name = request.form['name']
      type = request.form['type']
      address = request.form['address']
      email = request.form['email']
      phone = request.form['phone']
      FM.add_facility(name, type, address, email, phone)  
      return redirect(url_for('facilities'))
    elif a == 'edit':
      id = request.form['id']
      name = request.form['name']
      type = request.form['type']
      address = request.form['address']
      email = request.form['email']
      phone = request.form['phone']
      FM.edit_facility(id, name, type, address, email, phone)
      return redirect(url_for('facilities'))
    elif a == 'delete':
      id = request.form['id']
      FM.remove_facility(id)
      return redirect(url_for('facilities'))



# User Management - Page
# Userdata - username(50), password(100), name(50), role(20), email(320), phone(15)
@app.route('/usermanagement')
def usermanagement():
  session['page'] = 'usermanagement'
  return render_template('usermanagement.html', mode='view')

@app.route('/usermanagement/<a>', methods=['GET', 'POST'])
def usermanagement_mode(a):
  if a == 'newuser':
    return render_template('usermanagement.html', mode='adduser')
  
  elif a == 'adduser':
    username, password = request.form['username'], request.form['password']
    if UM.check_username(username):
      session['message'] = 'Username Already exists'
      return render_template('usermanagement.html', mode='adduser')
    return render_template('usermanagement.html', mode='adduser2', username=username, password=password)
  
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
  
  elif a == 'discard':
    return redirect(url_for('usermanagement'))
  
  elif a == 'edituser':
    username = request.form['username']
    try:
      user = UM.get_user(username)
      return render_template('usermanagement.html', mode='edit', username=user.USERNAME, 
                             name=user.name, role=user.role, 
                             email=user.email, phone=user.phone)
    except Exception as e:
      session['message'] = str(e)
    return redirect(url_for('usermanagement'))
  
  elif a == 'edituserconfirm':
    username = request.form['username']
    name = request.form['name']
    role = request.form['role']
    email = request.form['email']
    phone = request.form['phone']
    try:
      UM.edit_user(username, name, role, email, phone)
      return redirect(url_for('usermanagement'))
    except Exception as e:
      session['message'] = str(e)
      user = UM.get_user(username)
      return render_template('usermanagement.html', mode='edit', username=user.USERNAME, 
                             name=user.name, role=user.role, 
                             email=user.email, phone=user.phone)
    

  elif a == 'removeuser':
    username = request.form['username']
    UM.remove_user(username)
    return redirect(url_for('usermanagement'))

  else:
    return render_template('404.html')


# Profile - Page
@app.route('/profile')
def profile():
  session['page'] = 'profile'
  return render_template('profile.html', mode='view')

@app.route('/profile/<a>', methods=['POST', 'GET'])
def profile_mode(a):
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
        session['message'] = 'Password Incorrect'
        return render_template('profile.html', mode='view')
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
  return dict(UM=UM, FM=FM, SM=SM)



if __name__ == '__main__':
  app.config['SECRET_KEY'] = '123456789'
  app.run(debug=True)
