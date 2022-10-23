import ibm_db


class DB:
  def __init__(self):
    self.conn = ibm_db.connect('DATABASE=bludb;'
                               'HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;'
                               'PORT=30756;'
                               'SECURITY=SSL;'
                               'PROTOCOL=TCPIP;'
                               'UID=vtd38824;'
                               'PWD=xNA3fkYjTVqU5ac7;', '', '')

  def add(self, username, password, firstname, lastname, email, phone):
    sql = "insert into Userdata (USERNAME,PASSWORD,FIRSTNAME,LASTNAME,EMAIL,PHONE) values (?, ?, ?, ?, ?, ?);"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.bind_param(stmt, 3, firstname)
    ibm_db.bind_param(stmt, 4, lastname)
    ibm_db.bind_param(stmt, 5, email)
    ibm_db.bind_param(stmt, 6, phone)
    ibm_db.execute(stmt)
    
  def remove(self, username):
    sql = "delete from Userdata where username=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
  
  def get_data(self, username):
    sql = "select * from Userdata where username=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
    d = ibm_db.fetch_both(stmt)
    print(d)
    if d:
      return d
    return None
  
  def check_user(self, username, password):
    sql = "SELECT * FROM Userdata WHERE username=? AND password=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    d = ibm_db.fetch_both(stmt)
    if d:
      return True
    return False
  