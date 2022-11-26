USERPRIVILEGES = {'superadmin':-1, 'admin':0, 'user':1, 'visitor':2}


class User:
  def __init__(self, DB, USERNAME, PASSWORD, name, role, email, phone, new = False):
    self.DB = DB
    self.USERNAME = USERNAME
    self.PASSWORD = PASSWORD
    self.name = name
    self.role = role
    self.email = email
    self.phone = phone
    if new:
      self.DB.add_user(self.USERNAME, self.PASSWORD, self.name, self.role, self.email, self.phone)
  

  def pull(self):
    d = self.DB.get_user(self.USERNAME, self.PASSWORD)
    self.name = d['name']
    self.role = d['role']
    self.email = d['email']
    self.phone = d['phone']

    
  def push(self):
    self.DB.update_user(self.USERNAME, self.PASSWORD, self.name, self.role, self.email, self.phone)
  
  
  def privilege(self):
    return USERPRIVILEGES[self.role]
  
  
  def change_role(self, newrole):
    self.role = newrole

  
  def change_password(self, newpassword):
    self.DB.change_password(self.USERNAME, self.PASSWORD, newpassword)
    self.PASSWORD = newpassword


  def remove(self):
    self.DB.remove_user(self.USERNAME, self.PASSWORD)




class UserManagement:
  def __init__(self, DB):
    self.DB = DB
    self.users = None
    self.pull()
    
  
  def pull(self):
    users = []
    for i in self.DB.get_users():
      users.append(User(self.DB, i['username'], i['password'], i['name'], i['role'], i['email'], i['phone']))
    self.users = users
    
  
  def get_user(self, username):
    print("get_user:", username)
    for i in self.users:
      if i.USERNAME == username:
        return i
    raise Exception('User Not Found')
  
  
  def get_users(self):
    return self.users
  
  
  def check_user(self, username, password):
    for i in self.users:
      if i.USERNAME == username and i.PASSWORD == password:
        return True
    return False
  
  
  def check_username(self, username):
    for i in self.users:
      if i.USERNAME == username:
        return True
    return False
  
  
  def add_user(self, username, password, name, role, email, phone):
    self.users.append(User(self.DB, username, password, name, role, email, phone, new = True))
    
  
  def edit_user(self, username, newname=None, newrole=None, newemail=None, newphone=None):
    for i in self.users:
      if i.USERNAME == username:
        if newname: i.name = newname
        if newrole: i.change_role(newrole)
        if newemail: i.email = newemail
        if newphone: i.phone = newphone
        i.push()
        return
    raise Exception('User Not Found')
  
  
  def change_password(self, username, newpassword):
    for i in self.users:
      if i.USERNAME == username:
        i.change_password(newpassword)
        i.push()
        return
    raise Exception('User Not Found')
  
  
  def remove_user(self, username):
    for i in self.users:
      if i.USERNAME == username:
        print(1)
        i.remove()
        print(2)
        self.users.remove(i)
        return
    raise Exception('User Not Found')