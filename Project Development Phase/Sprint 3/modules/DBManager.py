import ibm_db

class DBManager():
    def __init__(self, dsn_hostname, dsn_port, dsn_uid, dsn_pwd):
        dsn_driver = "{IBM DB2 ODBC DRIVER}"
        dsn_database = "BLUDB"
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
        self.conn = ibm_db.connect(dsn, "", "")
        self.add_superadmin()

    def add_superadmin(self):
        if not self.check_username('superadmin'):
            self.add_user('superadmin', 'toor1234', 'Super Admin', 'superadmin', 'none', '0000')
                          

    #Userdata - username(50), password(100), name(30), role(20), email(320), phone(15)     
    def add_user(self, username, password, name, role, email, phone):        
        sql = f"""insert into userdata (username,password,name,role,email,phone)
                  values ('{username}','{password}','{name}','{role}','{email}','{phone}');"""
        try: ibm_db.exec_immediate(self.conn, sql)
        except: raise Exception("Username Already Exists")

    def get_user(self, username, password):
        sql = f"""select username,password,name,role,email,phone from userdata 
                            where username='{username}' and password='{password}';"""
        if i:=ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
            return {'username':i['USERNAME'],'password':i['PASSWORD'],'name':i['NAME'],
                            'role':i['ROLE'],'email':i['EMAIL'],'phone':i['PHONE']}
        raise Exception("Invalid Username or Password")

    def get_users(self):
        sql = f"""select username,password,name,role,email,phone from userdata;"""
        d = ibm_db.exec_immediate(self.conn, sql)
        while i:=ibm_db.fetch_both(d):
            yield {'username':i['USERNAME'],'password':i['PASSWORD'],'name':i['NAME'],
                   'role':i['ROLE'],'email':i['EMAIL'],'phone':i['PHONE']}

    def update_user(self, username, password, newname, newrole, newemail, newphone):
        if not self.check_user(username, password):
            raise Exception("Invalid Username or Password")
        sql = f"""update userdata set (name,role,email,phone) = 
                                ('{newname}','{newrole}','{newemail}','{newphone}')
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




    # facility - id(auto), name(30), type(20), address(100), email(320), phone(15)
    # stock - id(auto), name(30), type(20)(Grocery, Home Appliances, Stationary, Uncategorised), price(10,2), quantity, facility