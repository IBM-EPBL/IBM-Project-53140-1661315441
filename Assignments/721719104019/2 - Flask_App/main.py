from flask import Flask, render_template, request, session, redirect, url_for
import ibm_db

app = Flask(__name__)
HOSTNAME = "21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
PORT = 31864
UID = "wxq10827"
PWD = "ymVaT0kPM3W5j0g5"
conn = ibm_db.connect('DATABASE=bludb;'
                                f'HOSTNAME={HOSTNAME};'
                                f'PORT={PORT};'
                                 'SECURITY=SSL;'
                                 'PROTOCOL=TCPIP;'
                                f'UID={UID};'
                                f'PWD={PWD};', '', '')


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
    if session['win'] != 'signin':
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
    if session['win'] != 'signup':
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
            session['form'] = {'username': request.form['username'],
                               'password': request.form['password']}
            sql = f"SELECT * FROM assignment WHERE username='{session['form']['username']}' AND password='{session['form']['password']}'"
            d = ibm_db.fetch_both(ibm_db.exec_immediate(conn, sql))
            if d:
                data = d[0]
                session['userdb'] = {'username': data['USERNAME'],
                                     'name': data['NAME']}
                session.pop('form')
                session['win'] = session['tmp']
                return redirect(url_for('index'))
            else:
                session['msg'] = 'Invalid username or password'
                return redirect(url_for('index'))

        elif session['win'] == 'signup':
            session['form'] = {'username': request.form['username'],
                               'password': request.form['password'],
                               'name': request.form['name']}
            sql = f"SELECT * FROM assignment WHERE username='{session['form']['username']}'"
            d = ibm_db.fetch_both(ibm_db.exec_immediate(conn, sql))
            if d == None:
                sql = f"insert into Userdata (USERNAME,PASSWORD,name) values ('{session['form']['username']}','{session['form']['password']}','{session['form']['name']}');"
                ibm_db.fetch_both(ibm_db.exec_immediate(conn, sql))
                session['userdb'] = {'username': session['form']['username'],
                                     'name': session['form']['name']}
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
