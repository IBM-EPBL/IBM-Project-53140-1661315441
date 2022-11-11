from modules.dbmanager import DBManager


class User:
  def __init__(self, DB, username, password, name=None, role=None, email=None, phone=None, pre=False):
    self.DB = DB
    self.USERNAME = username
    self.PASSWORD = password
    self.npassword = None

    if all([name, role, email, phone]):  # Sign-up
      if not pre:
        DB.add_user(username, password, name, role, email, phone)
      self.name = name
      self.role = role
      self.email = email
      self.phone = phone
    else:  # Sign-in
      self.pull()

  def push(self):
    print('User.push(): USERNAME: %s, PASSWORD: %s, npassword: %s, name: %s, role: %s, email: %s, phone: %s' % (self.USERNAME, self.PASSWORD, self.npassword, self.name, self.role, self.email, self.phone))
    self.DB.update_user(self.USERNAME, self.PASSWORD, self.npassword,
              self.name, self.role, self.email, self.phone)
    self.npassword = None

  def pull(self):
    d = self.DB.get_user(self.USERNAME, self.PASSWORD)
    self.name = d['name']
    self.role = d['role']
    self.email = d['email']
    self.phone = d['phone']

  def remove(self):
    self.DB.remove_user(self.USERNAME, self.PASSWORD)


class UserManagement:
  def __init__(self, DB):
    self.DB = DB
    self.user = None

  def signin(self, username, password):
    print("UserManagement.signin(): username = %s, password = %s" %
              (username, password))
    self.user = User(self.DB, username, password)

  def signout(self):
    print("UserManagement.signout(): user = %s" % self.user)
    if self.user:
      self.user = None
    else:
      raise Exception("No user signed in")

  def signup(self, username, password, name, role, email, phone):
    print("UserManagement.signup(): username = %s, password = %s, name = %s, role = %s, email = %s, phone = %s" % (
      username, password, name, role, email, phone))
    self.user = User(self.DB, username, password, name, role, email, phone)

  def update(self, name, role, email, phone):
    print("UserManagement.update(): name = %s, role = %s, email = %s, phone = %s" % (
      name, role, email, phone))
    if not self.user:
      raise Exception("No user signed in")
    if name: self.user.name = name 
    if role: self.user.role = role
    if email: self.user.email = email
    if phone: self.user.phone = phone
    self.user.push()
  
  def update_password(self, password, npassword):
    print("UserManagement.update_password(): password = %s, npassword = %s" % (
      password, npassword))
    if not self.user:
      raise Exception("No user signed in")
    if self.user.PASSWORD != password:
      raise Exception("Incorrect old password")
    if self.user.PASSWORD == npassword:
      raise Exception("New password must be different from old password")
    self.user.npassword = npassword
    self.user.push()

  def remove_user(self):
    print("UserManagement.remove_user(): user = %s" % self.user.USERNAME)
    if not self.user:
      raise Exception("No user signed in")
    self.user.remove()
    self.user = None

  def get_users(self):
    return [User(self.DB, *d, pre=True) for d in self.DB.get_users() if d[3] != 'superadmin']
