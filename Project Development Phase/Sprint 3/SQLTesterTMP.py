import ibm_db

dsn_hostname = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "phd49688"
dsn_pwd = "0FVzO5GGOpX26adE"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "30376"
dsn_protocol = "TCPIP"
dsn_security = "SSL"
dsn = (f"DRIVER={dsn_driver};"
      f"DATABASE={dsn_database};"
      f"HOSTNAME={dsn_hostname};"
      f"PORT={dsn_port};"
      f"PROTOCOL={dsn_protocol};"
      f"UID={dsn_uid};"
      f"PWD={dsn_pwd};"
      f"SECURITY={dsn_security};")
print(dsn)
conn = None
try:
    conn = ibm_db.connect(dsn, "", "")
except:
    print("Unable to connect: ", ibm_db.conn_errormsg())

sql = "select * from userdata;"


try:
    a = ibm_db.exec_immediate(conn, sql)
    print('SQL Executed:', a)
    while b := ibm_db.fetch_both(a):
        print('Fetch Both: ', b)
except Exception as e:
    print('Exception Occured: ', ibm_db.stmt_errormsg())
    print('Exception Code: ', ibm_db.stmt_error())
