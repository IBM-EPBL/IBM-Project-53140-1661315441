import ibm_db


HOSTNAME = "6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 30376
SSLServerCertificate = 'DigiCertGlobalRootCA.crt'
UID = "szk22942"
PWD = "9tvjYOOk8eRYq5wu"
conn = ibm_db.connect('DATABASE=bludb;'
                              f'HOSTNAME={HOSTNAME};'
                              f'PORT={PORT};'
                               'SECURITY=SSL;'
                               'PROTOCOL=TCPIP;'
                              f'UID={UID};'
                              f'PWD={PWD};', '', '')


def check(sql):
  try:
    u = ibm_db.exec_immediate(conn,sql)
    print(u)
    print(ibm_db.fetch_both(u))
  except:
    print(ibm_db.stmt_error())
    print(ibm_db.stmt_errormsg())
