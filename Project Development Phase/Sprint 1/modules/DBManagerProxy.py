class DBManagerProxy():
  def __init__(self, HOSTNAME, PORT, UID, PWD):
    self.users = []

    
  # Userdata - username(50), password(100), name(50), role(20), email(320), phone(15)
  def add_user(self, username, password, name, role, email, phone):
    print("Adding User: " + str({'username':username,'password':password,'name':name,'role':role,'email':email,'phone':phone}))
    if self.check_username(username):
      raise Exception("Username Already Exists")
    self.users.append({'username':username,'password':password,'name':name,
                       'role':role,'email':email,'phone':phone})
  
  
  def get_user(self, username, password):
    print("Getting User: " + str({'username':username,'password':password}))
    for i in self.users:
      if i['username'] == username and i['password'] == password:
        return i
    raise Exception("Invalid Username or Password")
  
  
  def get_users(self):
    print("Getting Users:" + str(self.users))
    return self.users
    
  
  def update_user(self, username, password, newname, newrole, newemail, newphone):
    print("Updating User: " + str({'username':username,'password':password,'name':newname,'role':newrole,'email':newemail,'phone':newphone}))
    for i in self.users:
      if i['username'] == username and i['password'] == password:
        i['name'] = newname
        i['role'] = newrole
        i['email'] = newemail
        i['phone'] = newphone
        return
    raise Exception("Invalid Username or Password")
  
  
  def change_password(self, username, oldpassword, newpassword):
    print("Changing Password: " + str({'username':username,'oldpassword':oldpassword,'newpassword':newpassword}))
    for i in self.users:
      if i['username'] == username and i['password'] == oldpassword:
        i['password'] = newpassword
        return
    raise Exception("Invalid Username or Password")
  
  
  def remove_user(self, username, password):
    print("Removing User: " + str({'username':username,'password':password}))
    for i in self.users:
      if i['username'] == username and i['password'] == password:
        self.users.remove(i)
        return
    raise Exception("Invalid Username or Password")
  
  
  def check_username(self, username):
    print("Checking Username: " + username)
    for i in self.users:
      if i['username'] == username:
        return True
    return False
  
  
  def check_user(self, username, password):
    print("Checking User: " + str({'username':username,'password':password}))
    for i in self.users:
      if i['username'] == username and i['password'] == password:
        return True
    return False
  
  
  
  # workplace - id(auto), name(50), type(20), address(255), email(320), phone(15)
  # inventory - id, stockname(50), brand(30), varient(30), price(10,2), quantity, expirydate
  