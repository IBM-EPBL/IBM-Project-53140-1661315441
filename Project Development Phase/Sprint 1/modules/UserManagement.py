from modules.DBManager import DBManager

USERPRIVILEGES = {'superadmin':-1, 'admin':0, 'standarduser':1, 'user':1, 'visitor':2}

class User:
  def __init__(self, DB, USERNAME, PASSWORD, name=None, role=None, email=None, phone=None, pre=False):
    self.DB = DB
    self.USERNAME = USERNAME
    self.PASSWORD = PASSWORD
    self.privilege = None

    if all([name, role, email, phone]):  # Sign-up
      if not pre:
        DB.add_user(USERNAME, PASSWORD, name, role, email, phone)
      self.USERNAME = USERNAME
      self.name = name
      self.role = role
      self.email = email
      self.phone = phone
      self.privilege = USERPRIVILEGES[self.role]
    else:  # Sign-in
      self.pull()


  def pull(self):
    d = self.DB.get_user(self.USERNAME, self.PASSWORD)
    self.name = d['name']
    self.role = d['role']
    self.email = d['email']
    self.phone = d['phone']
    self.privilege = USERPRIVILEGES[self.role]

    
  def push(self):
    self.DB.update_user(self.USERNAME, self.PASSWORD, self.name, self.role, self.email, self.phone)

  
  def change_password(self, newpassword):
    self.DB.change_password(self.USERNAME, self.PASSWORD, newpassword)
    self.PASSWORD = newpassword


  def remove(self):
    self.DB.remove_user(self.USERNAME, self.PASSWORD)



class Profile:
  def __init__(self, DB):
    self.DB = DB
    self.user = None


  def signin(self, username, password):
    username = username.lower()
    self.user = User(self.DB, username, password)


  def signout(self):
    if not self.user:
      raise Exception("No User Signed in")
    self.user = None


  def update(self, name, email, phone):
    if not self.user:
      raise Exception("No User Signed in")
    if name: self.user.name = name
    if email: self.user.email = email
    if phone: self.user.phone = phone
    self.user.push()
  

  def update_password(self, password, newpassword):
    if not self.user:
      raise Exception("No User Signed in")
    if self.user.PASSWORD != password:
      raise Exception("Incorrect Old Password")
    if self.user.PASSWORD == newpassword:
      raise Exception("New Password must be Different from Old Password")
    self.user.change_password(newpassword)


  def remove_user(self, password):
    if not self.user:
      raise Exception("No User Signed in")
    if self.user.PASSWORD != password:
      raise Exception('Incorrect Password')
    self.user.remove()
    self.user = None



class UserManagement:
  def __init__(self, DB):
    self.DB = DB
  
  def get_users(self):
    return [User(self.DB, *d, pre=True) for d in self.DB.get_users()]
  
  def add_user(self, username, password, name, role, email, phone):
    DB.add_user(username, password, name, role, email, phone)
  
  def update_user(self, oldusername, oldpassword, password, name, role, email, phone):
    DB.update_user(oldusername, oldpassword, password, name, role, email, phone)
  
  def remove_user(self, username, password):
    DB.remove_user(username, password)
  