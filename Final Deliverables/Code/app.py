from flask import Flask, render_template, request, session, redirect, url_for
from modules.DBManager import DBManager
from modules.UserManagement import UserManagement
from modules.FacilityManagement import FacilityManagement
from modules.StockManagement import StockManagement
from modules.Constants import Constants
from modules.SendgridAPI import SendgridAPI
from modules.LogManagement import LogManagement

app = Flask(__name__)

DB = DBManager()
UM = UserManagement(DB)
FM = FacilityManagement(DB)
CON = Constants()
SG = SendgridAPI()
SM = StockManagement(DB, UM, FM, SG)
LM = LogManagement(DB, SM)

# Session Variables:
# page - The page the user is currently on
# message - The message to display to the user
# username - The username of the user
# sort - The column to sort the table by
# filter - The filter to apply to the table


# Root URL
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    session['page'] = 'dashboard'
    return render_template('home.html')


# Dashboard - Page
@app.route('/dashboard')
def dashboard():
    session['page'] = 'dashboard'
    return render_template('dashboard.html')


@app.route('/dashboard/clearlog')
def dashboard_clearlog():
    try:
        LM.clear_all_logs()
        session['message'] = 'All logs have been cleared'
    except Exception as e:
        session['message'] = 'Error: ' + str(e)
    return redirect(url_for('dashboard'))


# Stock - Page
# stock - id, name, type, price, quantity, facility
@app.route('/stock')
def stock():
    session['page'] = 'stock'
    if 'sort' not in session:
        session['sort'] = 'id'
    if 'sortorder' not in session:
        session['sortorder'] = 'asc'
    return render_template('stock.html', mode='view')


@app.route('/stock/<a>', methods=['GET', 'POST'])
def stock_mode(a):
    if a == 'view':
        return render_template('stock.html', mode='view')
    elif a == 'add':
        return render_template('stock.html', mode='add')
    elif a == 'update':
        id = request.form['id']
        quantity = request.form['quantity']
        try:
            SM.edit_quantity(id, quantity)
            return render_template('stock.html', mode='view')
        except Exception as e:
            session['message'] = 'Error: ' + str(e)
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
    if a == 'view':
        if b in CON.SORTBY:
            session['sort'] = b
        elif b in ('asc', 'desc'):
            session['sortorder'] = b
        else:
            return render_template('404.html')
        return redirect(url_for('stock'))
    if b == 'discard':
        return redirect(url_for('stock'))
    elif b == 'save':
        if a == 'add':
            try:
                name = request.form['name']
                type = request.form['type']
                price = request.form['price']
                quantity = request.form['quantity']
                minvalue = request.form['minvalue']
                facility = request.form['facility']
                SM.add_item(name, type, price, quantity, minvalue, facility)
                return redirect(url_for('stock'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('stock.html', mode='add')
        elif a == 'edit':
            try:
                id = request.form['id']
                name = request.form['name']
                type = request.form['type']
                price = request.form['price']
                quantity = request.form['quantity']
                minvalue = request.form['minvalue']
                facility = request.form['facility']
                SM.edit_item(id, name, type, price,
                             quantity, minvalue, facility)
                return redirect(url_for('stock'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('stock.html', mode='edit', id=id)
        elif a == 'delete':
            try:
                id = request.form['id']
                SM.remove_item(id)
                return redirect(url_for('stock'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('stock.html', mode='delete', id=id)
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
        return render_template('facilities.html', mode='edit', id=id)
    elif a == 'delete':
        id = request.form['id']
        return render_template('facilities.html', mode='delete', id=id)
    else:
        return render_template('404.html')


@app.route('/facilities/<a>/<b>', methods=['GET', 'POST'])
def facilities_action(a, b):
    if b == 'discard':
        return redirect(url_for('facilities'))
    elif b == 'save':
        if a == 'add':
            try:
                name = request.form['name']
                type = request.form['type']
                address = request.form['address']
                email = request.form['email']
                phone = request.form['phone']
                FM.add_facility(name, type, address, email, phone)
                return redirect(url_for('facilities'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('facilities.html', mode='add')
        elif a == 'edit':
            try:
                id = request.form['id']
                name = request.form['name']
                type = request.form['type']
                address = request.form['address']
                email = request.form['email']
                phone = request.form['phone']
                FM.edit_facility(id, name, type, address, email, phone)
                return redirect(url_for('facilities'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('facilities.html', mode='edit', id=id)
        elif a == 'delete':
            try:
                id = request.form['id']
                FM.remove_facility(id)
                return redirect(url_for('facilities'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('facilities.html', mode='delete', id=id)


# User Management - Page
# Userdata - username(50), password(100), name(50), role(20), email(320), phone(15)
@app.route('/usermanagement')
def usermanagement():
    session['page'] = 'usermanagement'
    return render_template('usermanagement.html', mode='view')


# Modes - view, add, add2, edit, delete
@app.route('/usermanagement/<a>', methods=['GET', 'POST'])
def usermanagement_mode(a):
    if a == 'add':
        return render_template('usermanagement.html', mode='add', username='', password='')
    elif a == 'edit':
        username = request.form['username']
        return render_template('usermanagement.html', mode='edit', username=username)
    elif a == 'delete':
        username = request.form['username']
        return render_template('usermanagement.html', mode='delete', username=username)
    else:
        return render_template('404.html')


@app.route('/usermanagement/<a>/<b>', methods=['GET', 'POST'])
def usermanagement_action(a, b):
    if b == 'discard':
        if a == 'add2':
            username = request.form['username']
            password = request.form['password']
            return render_template('usermanagement.html', mode='add', username=username, password=password)
        return redirect(url_for('usermanagement'))
    elif b == 'save':
        if a == 'add':
            username = request.form['username']
            password = request.form['password']
            return render_template('usermanagement.html', mode='add2', username=username, password=password)
        elif a == 'add2':
            try:
                username = request.form['username']
                password = request.form['password']
                name = request.form['name']
                role = request.form['role']
                email = request.form['email']
                phone = request.form['phone']
                UM.add_user(username, password, name, role, email, phone)
                return redirect(url_for('usermanagement'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('usermanagement.html', mode='add2', username=username, password=password)
        elif a == 'edit':
            try:
                username = request.form['username']
                name = request.form['name']
                role = request.form['role']
                email = request.form['email']
                phone = request.form['phone']
                UM.edit_user(username, name, role, email, phone)
                return redirect(url_for('usermanagement'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('usermanagement.html', mode='edit', username=username)
        elif a == 'delete':
            try:
                username = request.form['username']
                UM.remove_user(username)
                return redirect(url_for('usermanagement'))
            except Exception as e:
                session['message'] = 'Error: ' + str(e)
                return render_template('usermanagement.html', mode='delete', username=username)
    else:
        return render_template('404.html')


# Profile - Page
@app.route('/profile')
def profile():
    session['page'] = 'profile'
    return render_template('profile.html', mode='view')


# Modes: view, edit, changepassword
@app.route('/profile/<a>', methods=['POST', 'GET'])
def profile_mode(a):
    if a == 'edit':
        return render_template('profile.html', mode='edit')
    elif a == 'changepassword':
        return render_template('profile.html', mode='changepassword')
    elif a == 'remove':
        try:
            password = request.form['password']
            if not UM.check_user(session['username'], password):
                session['message'] = 'Password Incorrect'
                return redirect(url_for('profile'))
            UM.remove_user(session['username'])
            session.pop('username', None)
            session['message'] = 'User Removed Successfully'
            return redirect(url_for('signin'))
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
    else:
        return render_template('404.html')


@app.route('/profile/<a>/<b>', methods=['POST', 'GET'])
def profile_action(a, b):
    if b == 'discard':
        return redirect(url_for('profile'))
    elif b == 'save':
        if a == 'edit':
            try:
                name, email, phone = request.form['name'], request.form['email'], request.form['phone']
                UM.edit_user(
                    username=session['username'], newname=name, newemail=email, newphone=phone)
                return redirect(url_for('profile'))
            except Exception as e:
                session['message'] = str(e)
            return render_template('profile.html', mode='edit')
        elif a == 'changepassword':
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
        else:
            return render_template('404.html')
    else:
        return render_template('404.html')


# Sign In - Page
@app.route('/signin')
def signin():
    if 'user' in session:
        session['message'] = 'You are already Signed in'
        return redirect(url_for(session['page']))
    return render_template('signin.html')


@app.route('/signin/handle_form', methods=['POST', 'GET'])
def signin_action():
    try:
        username, password = request.form['username'], request.form['password']
        if UM.check_user(username, password):
            session['username'] = username
            return redirect(url_for(session['page']))
        else:
            session['message'] = 'Invalid Username or Password'
            return redirect('/')
    except Exception as e:
        session['message'] = str(e)
        return redirect('/signin')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def inject_data():
    return dict(UM=UM, FM=FM, SM=SM, CON=CON, LM=LM)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = '123456789'
    app.run(debug=True, port=5050)
