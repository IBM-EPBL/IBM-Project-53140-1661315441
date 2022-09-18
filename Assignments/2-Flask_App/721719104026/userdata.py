import sqlite3


class DB:
  def __init__(self):
    self.conn = sqlite3.connect('userdata.db')
    self.conn.execute('''
                      CREATE TABLE IF NOT EXISTS
                      Userdata(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      firstname TEXT NOT NULL,
                      lastname TEXT NOT NULL,
                      email TEXT NOT NULL,
                      password TEXT NOT NULL)
                      ''')
  
  def add(self, username, firstname, lastname, email, password):
    self.conn.execute('''
                      INSERT INTO Userdata(username, firstname, lastname, email, password)
                      VALUES(?, ?, ?, ?, ?)
                      ''', (username, firstname, lastname, email, password))
    self.conn.commit()
    
  def get(self, username):
    cursor = self.conn.execute('''
                               SELECT * FROM Userdata WHERE username = ?
                               ''', (username,))
    return cursor.fetchone()
  
  def check_user(self, username, password):
    cursor = self.conn.execute('''
                               SELECT * FROM Userdata WHERE username = ? AND password = ?
                               ''', (username, password))
    return cursor.fetchone() is not None
  
  def check_username(self, username):
    cursor = self.conn.execute('''
                               SELECT * FROM Userdata WHERE username = ?
                               ''', (username,))
    return cursor.fetchone() is None
