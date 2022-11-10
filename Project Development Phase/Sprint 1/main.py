from flask import Flask, render_template, request, session, redirect, url_for
from modules.dbmanager import DBManager

app = Flask(__name__)
HOSTNAME = "21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
PORT = 31864
SSLServerCertificate = 'DigiCertGlobalRootCA.crt'
UID = "wxq10827"
PWD = "ymVaT0kPM3W5j0g5"
DB = DBManager(HOSTNAME, PORT, SSLServerCertificate, UID, PWD)


if __name__ == '__main__':
  app.config['SECRET_KEY'] = '123456789'
  app.run(debug=True)
