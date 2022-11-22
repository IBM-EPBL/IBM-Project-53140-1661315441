import ibm_db

class DB:
  def __init__(self):
    self.conn = ibm_db.connect('DATABASE=bludb;'
                               'HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;'
                               'PORT=30376;'
                               'SECURITY=SSL;'
                               'PROTOCOL=TCPIP;'
                               'UID=SZK22942;'
                               'PWD=aeFNIczT3dPM6k6X;', '', '')

  def add(self, username, password):
    sql = "insert into ASSIGNMENT (USERNAME,PASSWORD) values (?, ?);"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    
  def remove(self, username):
    sql = "delete from ASSIGNMENT where username=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
  
  def get_data(self, username):
    sql = "select * from ASSIGNMENT where username=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
    d = ibm_db.fetch_both(stmt)
    print(d)
    if d:
      return d
    return None
  
  def check_user(self, username, password):
    sql = "SELECT * FROM ASSIGNMENT WHERE username=? AND password=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    d = ibm_db.fetch_both(stmt)
    if d:
      return True
    return False
  