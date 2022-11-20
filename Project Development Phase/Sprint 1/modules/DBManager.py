import ibm_db

class DBManager():
  def __init__(self, HOSTNAME, PORT, SSLServerCertificate, UID, PWD):
    self.conn = ibm_db.connect('DATABASE=bludb;'
                              f'HOSTNAME={HOSTNAME};'
                              f'PORT={PORT};'
                               'SECURITY=SSL;'
                               'PROTOCOL=TCPIP;'
                              f'UID={UID};'
                              f'PWD={PWD};', '', '')

    
  # Userdata - username(50), password(100), name(50), role(20), email(320), phone(15)
  def add_user(self, username, password, name, role, email, phone):
    sql = f"""insert into userdata (username,password,name,role,email,phone) 
              values ('{username}','{password}','{name}','{role}','{email}','{phone}');"""
    try: ibm_db.exec_immediate(self.conn, sql)
    except:
      if ibm_db.stmt_error() == '23505':
        raise Exception("Username Already Exists")
      else:
        raise Exception(ibm_db.stmt_errormsg())
  
  
  def get_user(self, username, password):
    sql = f"""select username,name,role,email,phone from userdata 
              where username='{username}' and password='{password}';"""
    if d:=ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
      return {'username':d['USERNAME'],'name':d['NAME'],
              'role':d['ROLE'],'email':d['EMAIL'],'phone':d['PHONE']}
    raise Exception("Invalid Username or Password")
  
  
  def get_users(self):
    sql = "select username,name,role,email,phone from userdata;"
    d = ibm_db.exec_immediate(self.conn, sql)
    l = []
    while i:=ibm_db.fetch_both(d):
      l.append({'username':i['USERNAME'],'name':i['NAME'],
                'role':i['ROLE'],'email':i['EMAIL'],'phone':i['PHONE']})
    return l
      
      
  def update_user(self, username, password, name, role, email, phone):
    if not self.check_user(username, password):
      raise Exception("Invalid Username or Password")
    sql = f"""update userdata set (name,role,email,phone) = 
                ('{name}','{role}','{email}','{phone}')
                where username='{username}' and password='{password}';"""
    ibm_db.exec_immediate(self.conn, sql)
  
  
  def change_password(self, username, oldpassword, newpassword):
    if not self.check_user(username, oldpassword):
      raise Exception("Invalid Username or Password")
    sql = f"""update userdata set password='{newpassword}' 
              where username='{username}' and password='{oldpassword}';"""
    ibm_db.exec_immediate(self.conn, sql)
  
  
  def remove_user(self, username, password):
    if not self.check_user(username, password):
      raise Exception("Invalid Username or Password")
    sql = f"delete from userdata where username='{username}' and password='{password}';"
    ibm_db.exec_immediate(self.conn, sql)
  
  
  def check_username(self, username):
    sql = f"select username from userdata where username='{username}';"
    return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False
  
  
  def check_user(self, username, password):
    sql = f"select username from userdata where username='{username}' and password='{password}';"
    return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False
  
  
  
  # workplace - id(auto), name(50), type(20), address(255), email(320), phone(15)
  def add_workplace(self, name, type, address, email, phone):
    sql = f"""insert into workplace (name,type,address,email,phone) 
              values ('{name}','{type}','{address}','{email}','{phone}');"""
    ibm_db.exec_immediate(self.conn, sql)
  
  def get_workplace(self, id):
    sql = f"select * from workplace where id={workplaceid};"
    if d:=ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
      return {id:d['ID'],name:d['NAME'],type:d['TYPE'],address:d['ADDRESS'],
              email:d['EMAIL'],phone:d['PHONE']}
    raise Exception("Invalid workplace id")

  def update_workplace(self, id, name, type, address, email, phone):
    if not self.check_workspace(id):
      raise Exception("Invalid workplace id")
    sql = f"""update workplace set (name,type,address,email,phone) 
              = ('{name}','{type}','{address}','{email}','{phone}')
              where id={id};"""
    ibm_db.exec_immediate(self.conn, sql)
  
  def remove_workplace(self, id):
    if not self.check_workspace(id):
      raise Exception("Invalid workplace id")
    sql = f"delete from workplace where id={id};"
    ibm_db.exec_immediate(self.conn, sql)
  
  def check_workspace(self, id):
    sql = f"select * from inventory where id={id};"
    return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False
  
  
  # inventory - id, stockname(50), brand(30), varient(30), price(10,2), quantity, expirydate
  def add_inventory(self, id, stockname, brand, varient, price, quantity, expirydate):
    sql = f"""insert into inventory (id,stockname,brand,varient,price,quantity,expirydate) 
              values ({id},'{stockname}','{brand}','{varient}',{price},{quantity},'{expirydate}');"""
    ibm_db.exec_immediate(self.conn, sql)
  
  def get_inventory(self, id):
    sql = f"select * from inventory where id={id};"
    if d:=ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
      return {id:d['ID'],stockname:d['STOCKNAME'],brand:d['BRAND'],varient:d['VARIENT'],
              price:d['PRICE'],quantity:d['QUANTITY'],expirydate:d['EXPIRYDATE']}
    raise Exception("Invalid inventory id")

  def update_inventory(self, id, stockname, brand, varient, price, quantity, expirydate):
    if not self.check_inventory(id):
      raise Exception("Invalid inventory id")
    sql = f"""update inventory set (stockname,brand,varient,price,quantity,expirydate) 
              = ('{stockname}','{brand}','{varient}',{price},{quantity},'{expirydate}')
              where id={id};"""
    ibm_db.exec_immediate(self.conn, sql)
  
  def remove_inventory(self, id):
    if not self.check_inventory(id):
      raise Exception("Invalid inventory id")
    sql = f"delete from inventory where id={id};"
    ibm_db.exec_immediate(self.conn, sql)
  
  def check_inventory(self, id):
    sql = f"select * from inventory where id={id};"
    return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False


# TODO - Delete Credentials
HOSTNAME = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30376
SSLServerCertificate = 'DigiCertGlobalRootCA.crt'
UID = "szk22942"
PWD = "9tvjYOOk8eRYq5wu"
db = DBManager(HOSTNAME, PORT, 'asdsf', UID, PWD)
