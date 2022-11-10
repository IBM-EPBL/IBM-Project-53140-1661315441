import ibm_db

class DBManager():
  def __init__(self, HOSTNAME, PORT, UID, PWD):
    try:
      self.conn = ibm_db.connect('DATABASE=bludb;'
                                f'HOSTNAME={HOSTNAME};'
                                f'PORT={PORT};'
                                 'SECURITY=SSL;'
                                 'PROTOCOL=TCPIP;'
                                f'UID={UID};'
                                f'PWD={PWD};', '', '')
    except:     
      print("no connection:", ibm_db.conn_errormsg())
    else:
      print("The connection was successful")

    
  # Userdata - username(50), password(50), name(50), role(20), email(320), phone(15)
  def add_user(self, username, password, name, role, email, phone):
    sql = f"""insert into userdata (username,password,name,role,email,phone) 
              values ('{username}','{password}','{name}','{role}','{email}','{phone}');"""
    try: ibm_db.exec_immediate(self.conn, sql)
    except: raise Exception("Username already exists")
  
  def get_user(self, username, password):
    sql = f"select * from userdata where username='{username}' and password='{password}';"
    if d:=ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
      return {'username':d['USERNAME'],'password':d['PASSWORD'],'name':d['NAME'],
              'role':d['ROLE'],'email':d['EMAIL'],'phone':d['PHONE']}
    raise Exception("Invalid username or password")
  
  def update_user(self, oldusername, oldpassword, password, name, role, email, phone):
    if not self.check_user(oldusername, oldpassword):
      raise Exception("Invalid username or password")
    sql = f"""update userdata set (password,name,role,email,phone) 
              = ('{password}','{name}','{role}','{email}','{phone}')
              where username='{oldusername}' and password='{oldpassword}';"""
    ibm_db.exec_immediate(self.conn, sql)
  
  def remove_user(self, username, password):
    if not self.check_user(username, password):
      raise Exception("Invalid username or password")
    sql = f"delete from userdata where username='{username}' and password='{password}';"
    ibm_db.exec_immediate(self.conn, sql)
  
  def check_user(self, username, password):
    sql = f"select * from userdata where username='{username}' and password='{password}';"
    return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False

  def check_username(self, username):
    sql = f"select * from userdata where username='{username}';"
    return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False
  
  def get_users(self):
    sql = "select * from userdata;"
    d = ibm_db.exec_immediate(self.conn, sql)
    l = []
    while i:=ibm_db.fetch_both(d):
      l.append((i['USERNAME'],i['PASSWORD'],i['NAME'],i['ROLE'],i['EMAIL'],i['PHONE']))
    return l
