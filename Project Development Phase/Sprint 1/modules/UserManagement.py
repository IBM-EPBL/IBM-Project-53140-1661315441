from modules.DBManager import DBManager

USERPRIVILEGES = {'superadmin':-1, 'admin':0, 'user':1, 'visitor':2}

class User:
  def __init__(self, DB, USERNAME, PASSWORD, name=None, role=None, email=None, phone=None, pre=False):
    self.DB = DB
    self.USERNAME = USERNAME
    self.PASSWORD = PASSWORD
    self.privilege = None

    if all([name, role, email, phone]):  # Sign-up
      if not pre:
        DB.add_user(USERNAME, PASSWORD, name, role, email, phone)
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
    self.PR = None
    self.users = []
    
  
  def pull(self, PR):
    if PR.privilege < 1:
      self.PR = PR
      for i in self.DB.get_users_with_password(PR.user.USERNAME, PR.user.PASSWORD):
        self.users.append(User(self.DB, i['username'], i['password'], i['name'], 
                               i['role'], i['email'], i['phone'], pre=True))
    else:
      self.PR = None
      self.users = []
  
  
  def get_users(self):
    if not self.PR:
      raise Exception("No Admin Signed in")
    return self.users
  
  def get_user(self, username):
    for user in self.users:
      if user.USERNAME == username:
        return user
    raise Exception("User Not Found")
      
  
  def add_user(self, username, password, name, role, email, phone):
    if not self.PR:
      raise Exception("No Admin Signed in")
    if role == 'superadmin':
      raise Exception("Cannot Create Super Admin")
    if role == 'admin' and self.PR.user.privilege >= 0:
      raise Exception("Only Super Admin can Create Admin")
    user = User(self.DB, username, password, name, role, email, phone)
    self.users.append(user)
  
  
  def update_user(self, username, password, name, role, email, phone):
    user = None
    for i in self.users:
      if i.USERNAME == username:
        user = i
        break
    else:
      raise Exception("User Not Found")
    if not password: password = user.PASSWORD
    if not name: name = user.name
    if not role: role = user.role
    if not email: email = user.email
    if not phone: phone = user.phone
    
    if not self.PR:
      raise Exception("No Admin Signed in")
    if self.PR.user.USERNAME == username and self.PR.user.role == 'superadmin':
      raise Exception("Cannot Update Self Superadmin from Here")
    if role == 'superadmin':
      raise Exception("Cannot Update to Super Admin")
    if (role == 'admin' or user.role == 'admin') and self.PR.user.privilege >= 0:
      raise Exception("Only Super Admin can Update Admin")
    
    user.push()
  
  
  def remove_user(self, username):
    user = None
    for i in self.users:
      if i.USERNAME == username:
        user = i
        break
    else:
      raise Exception("User Not Found")
    
    if not self.PR:
      raise Exception("No Admin Signed in")
    if self.PR.user.USERNAME == username:
      raise Exception("Cannot Remove Self from Here")
    if self.PR.user.USERNAME == username and self.PR.user.role == 'superadmin':
      raise Exception("Cannot Remove Superadmin")
    
    self.users.remove(user)
    user.remove()
  