import os
import ibm_db


class DBManager():
    def __init__(self):
        dsn_hostname = os.environ.get('IBM_DB2_HOSTNAME')
        dsn_port = os.environ.get('IBM_DB2_PORT')
        dsn_uid = os.environ.get('IBM_DB2_UID')
        dsn_pwd = os.environ.get('IBM_DB2_PWD')
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
            self.add_user('superadmin', 'toor1234', 'Super Admin',
                          'superadmin', 'none', '0000')

    #Userdata - username(50), password(100), name(30), role(20), email(320), phone(15)

    def add_user(self, username, password, name, role, email, phone):
        sql = f"""insert into userdata (username,password,name,role,email,phone)
                  values ('{username}','{password}','{name}','{role}','{email}','{phone}');"""
        try:
            ibm_db.exec_immediate(self.conn, sql)
        except:
            raise Exception("Username Already Exists")

    def get_user(self, username, password):
        sql = f"""select username,password,name,role,email,phone from userdata 
                            where username='{username}' and password='{password}';"""
        if i := ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
            return {'username': i['USERNAME'], 'password': i['PASSWORD'], 'name': i['NAME'],
                    'role': i['ROLE'], 'email': i['EMAIL'], 'phone': i['PHONE']}
        raise Exception("Invalid Username or Password")

    def get_users(self):
        sql = f"""select username,password,name,role,email,phone from userdata;"""
        d = ibm_db.exec_immediate(self.conn, sql)
        while i := ibm_db.fetch_both(d):
            yield {'username': i['USERNAME'], 'password': i['PASSWORD'], 'name': i['NAME'],
                   'role': i['ROLE'], 'email': i['EMAIL'], 'phone': i['PHONE']}

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

    def add_facility(self, name, type, address, email, phone):
        sql = f"""insert into facility (name,type,address,email,phone)
                    values ('{name}','{type}','{address}','{email}','{phone}');"""
        ibm_db.exec_immediate(self.conn, sql)
        sql = f"select id from facility where name='{name}' and type='{type}' and address='{address}' and email='{email}' and phone='{phone}';"
        if i := ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
            return i['ID']
        raise Exception("Unable to add facility")

    def get_facility(self, id):
        sql = f"select id,name,type,address,email,phone from facility where id={id};"
        if i := ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
            return {'id': i['ID'], 'name': i['NAME'], 'type': i['TYPE'],
                    'address': i['ADDRESS'], 'email': i['EMAIL'], 'phone': i['PHONE']}
        raise Exception("Invalid Facility ID")

    def get_facilities(self):
        sql = f"select id,name,type,address,email,phone from facility;"
        d = ibm_db.exec_immediate(self.conn, sql)
        while i := ibm_db.fetch_both(d):
            yield {'id': i['ID'], 'name': i['NAME'], 'type': i['TYPE'],
                   'address': i['ADDRESS'], 'email': i['EMAIL'], 'phone': i['PHONE']}

    def update_facility(self, id, newname, newtype, newaddress, newemail, newphone):
        if not self.check_facility(id):
            raise Exception("Invalid Facility ID")
        sql = f"""update facility set (name,type,address,email,phone) = 
                  ('{newname}','{newtype}','{newaddress}','{newemail}','{newphone}')
                  where id={id};"""
        ibm_db.exec_immediate(self.conn, sql)

    def remove_facility(self, id):
        if not self.check_facility(id):
            raise Exception("Invalid Facility ID")
        sql = f"delete from facility where id={id};"
        ibm_db.exec_immediate(self.conn, sql)

    def check_facility(self, id):
        sql = f"select id from facility where id={id};"
        return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False

    # stock - id(auto), name(30), type(20)(Grocery, Home Appliances, Stationary, Uncategorised), price(10,2), quantity, minvalue, facility

    def add_item(self, name, type, price, quantity, minvalue, facility):
        sql = f"""insert into stock (name,type,price,quantity,minvalue,facility)
                    values ('{name}','{type}',{price},{quantity},{minvalue},{facility});"""
        ibm_db.exec_immediate(self.conn, sql)
        sql = f"select id from stock where name='{name}' and type='{type}' and price={price} and quantity={quantity} and minvalue={minvalue} and facility={facility};"
        if i := ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
            return i['ID']
        raise Exception("Unable to add item")

    def get_item(self, id):
        sql = f"select id,name,type,price,quantity,minvalue,facility from stock where id={id};"
        if i := ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)):
            return {'id': i['ID'], 'name': i['NAME'], 'type': i['TYPE'], 'price': i['PRICE'],
                    'quantity': i['QUANTITY'], 'minvalue': i['MINVALUE'], 'facility': i['FACILITY']}
        raise Exception("Invalid Item ID")

    def get_items(self):
        sql = f"select id,name,type,price,quantity,minvalue,facility from stock;"
        d = ibm_db.exec_immediate(self.conn, sql)
        while i := ibm_db.fetch_both(d):
            yield {'id': i['ID'], 'name': i['NAME'], 'type': i['TYPE'], 'price': i['PRICE'],
                   'quantity': i['QUANTITY'], 'minvalue': i['MINVALUE'], 'facility': i['FACILITY']}

    def update_item(self, id, newname, newtype, newprice, newquantity, newminvalue, newfacility):
        if not self.check_item(id):
            raise Exception("Invalid Item ID")
        sql = f"""update stock set (name,type,price,quantity,minvalue,facility) = 
                  ('{newname}','{newtype}',{newprice},{newquantity},{newminvalue},{newfacility})
                  where id={id};"""
        ibm_db.exec_immediate(self.conn, sql)

    def remove_item(self, id):
        if not self.check_item(id):
            raise Exception("Invalid Item ID")
        sql = f"delete from stock where id={id};"
        ibm_db.exec_immediate(self.conn, sql)

    def check_item(self, id):
        sql = f"select id from stock where id={id};"
        return True if ibm_db.fetch_both(ibm_db.exec_immediate(self.conn, sql)) else False

    # log - id(auto), facility, item, price, quantity, action(added, sold), timestamp(auto)

    def add_log(self, facility, item, price, quantity, action):
        sql = f"""insert into log (facility,item,price,quantity,action)
                  values ({facility},{item},{price},{quantity},'{action}');"""
        ibm_db.exec_immediate(self.conn, sql)

    def get_top_sold(self, limit):
        sql = f"""select item,sum(quantity) as quantity,sum(price*quantity) as revenue from log 
                  where action='sold' group by item order by revenue desc limit {limit};"""
        d = ibm_db.exec_immediate(self.conn, sql)
        while i := ibm_db.fetch_both(d):
            yield {'item': i['ITEM'], 'quantity': i['QUANTITY'], 'revenue': i['REVENUE']}

    def get_today_logs(self):
        sql = f"""select id,facility,item,price,quantity,action,timestamp from log 
                  where timestamp > current_date;"""
        d = ibm_db.exec_immediate(self.conn, sql)
        while i := ibm_db.fetch_both(d):
            yield {'id': i['ID'], 'facility': i['FACILITY'], 'item': i['ITEM'], 'price': i['PRICE'],
                   'quantity': i['QUANTITY'], 'action': i['ACTION'], 'timestamp': i['TIMESTAMP']}

    def clear_all_logs(self):
        sql = f"delete from log;"
        ibm_db.exec_immediate(self.conn, sql)
