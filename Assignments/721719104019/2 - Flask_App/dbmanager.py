import ibm_db

class DB:
  def __init__(self):
    self.conn = ibm_db.connect('DATABASE=bludb;'
                               'HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;'
                               'PORT=32733;'
                               'SECURITY=SSL;'
                               'PROTOCOL=TCPIP;'
                               'UID=hfx07302;'
                               'PWD=IKhcJPLkVrBcyGZN;', '', '')

  def add(self, username, password):
    sql = "insert into SIGNIN (USERNAME,PASSWORD) values (?, ?);"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    
  def remove(self, username):
    sql = "delete from SIGNIN where username=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
  
  def get_data(self, username):
    sql = "select * from SIGNIN where username=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
    d = ibm_db.fetch_both(stmt)
    print(d)
    if d:
      return d
    return None
  
  def check_user(self, username, password):
    sql = "SELECT * FROM SIGNIN WHERE username=? AND password=?"
    stmt = ibm_db.prepare(self.conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    d = ibm_db.fetch_both(stmt)
    if d:
      return True
    return False
  
