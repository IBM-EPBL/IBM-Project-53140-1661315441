class DBManagerProxy():
  def __init__(self, HOSTNAME, PORT, UID, PWD):
    self.users = [{'username':'superadmin', 'password':'toor1234', 'name':'Super Admin', 'role':'superadmin', 'email':'', 'phone':''},
                  {'username':'dhinesh', 'password':'helloworld', 'name':'Dhinesh', 'role':'admin', 'email':'dhinesh88825@gmail.com', 'phone':'0987654321'}]
    self.facilities = [{'id':'0', 'name':'Mohan Maligai', 'type':'store', 'address':'1, Sudarsan Nagar, Mahalingapuram, Pollachi', 'email':'mohan0472@gmail.com', 'phone':'0987654321'},
                       {'id':'1', 'name':'Sri Ganesh Stores', 'type':'store', 'address':'2, Sudarsan Nagar, Mahalingapuram, Pollachi', 'email':'ganesh@gmail.com', 'phone':'1234567890'}]
    self.items = [{'id':'0', 'name':'Milk', 'type':'dairy', 'price':'30', 'quantity':'10', 'expirydate':'01-01-2023', 'facility':'0'},
                  {'id':'1', 'name':'Eggs', 'type':'dairy', 'price':'10', 'quantity':'20', 'expirydate':'01-01-2023', 'facility':'0'}]

  
    
    
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
  
  
  
  
  # facility - id(auto), name(50), type(20), address(255), email(320), phone(15)
  def add_facility(self, name, type, address, email, phone):
    print("Adding Facility: " + str({'name':name,'type':type,'address':address,'email':email,'phone':phone}))
    self.facilities.append({'id':str(len(self.facilities)),'name':name,'type':type,'address':address,'email':email,'phone':phone})
    return str(len(self.facilities)-1)
  
  
  def get_facility(self, id):
    print("Getting Facility: " + str({'id':id}))
    for i in self.facilities:
      if i['id'] == id:
        return i
    raise Exception("Invalid Facility ID")
  
  
  def get_facilities(self):
    print("Getting Facilities:" + str(self.facilities))
    return self.facilities
  
  
  def update_facility(self, id, newname, newtype, newaddress, newemail, newphone):
    print("Updating Facility: " + str({'id':id,'name':newname,'type':newtype,'address':newaddress,'email':newemail,'phone':newphone}))
    for i in self.facilities:
      if i['id'] == id:
        i['name'] = newname
        i['type'] = newtype
        i['address'] = newaddress
        i['email'] = newemail
        i['phone'] = newphone
        return
    raise Exception("Invalid Facility ID")
  
  
  def remove_facility(self, id):
    print("Removing Facility: " + str({'id':id}))
    for i in self.facilities:
      if i['id'] == id:
        self.facilities.remove(i)
        return
    raise Exception("Invalid Facility ID")
    
  
  def check_facility(self, id):
    print("Checking Facility: " + str({'id':id}))
    for i in self.facilities:
      if i['id']==id:
        return True
    return False
  
  
  
  
  # inventory - id, name(50), type(30), price(10,2), quantity, expirydate, facility
  def add_item(self, name, type, price, quantity, expirydate, facility):
    print("Adding Item: " + str({'name':name,'type':type,'price':price,'quantity':quantity,'expirydate':expirydate,'facility':facility}))
    self.items.append({'id':str(len(self.items)),'name':name,'type':type,'price':price,'quantity':quantity,'expirydate':expirydate,'facility':facility})
    return str(len(self.items)-1)
  
  
  def get_item(self, id):
    print("Getting Item: " + str({'id':id}))
    for i in self.items:
      if i['id'] == id:
        return i
    raise Exception("Invalid Item ID")
  
  
  def get_items(self):
    print("Getting Items:" + str(self.items))
    return self.items
  
  
  def update_item(self, id, newname, newtype, newprice, newquantity, newexpirydate, newfacility):
    print("Updating Item: " + str({'id':id,'name':newname,'type':newtype,'price':newprice,'quantity':newquantity,'expirydate':newexpirydate,'facility':newfacility}))
    for i in self.items:
      if i['id'] == id:
        i['name'] = newname
        i['type'] = newtype
        i['price'] = newprice
        i['quantity'] = newquantity
        i['expirydate'] = newexpirydate
        i['facility'] = newfacility
        return
    raise Exception("Invalid Item ID")
  
  
  def remove_item(self, id):
    print("Removing Item: " + str({'id':id}))
    for i in self.items:
      if i['id'] == id:
        self.items.remove(i)
        return
    raise Exception("Invalid Item ID")