class Stock:
  def __init__(self, DB, id, name, type, price, quantity, expirydate, facility, new=False):
    self.DB = DB
    self.id = id
    self.name = name
    self.type = type
    self.price = price
    self.quantity = quantity
    self.expirydate = expirydate
    self.facility = facility
    if new:
      self.id = self.DB.add_item(self.name, self.type, self.price, self.quantity, self.expirydate, self.facility)
    
  def pull(self):
    d = self.DB.get_item(self.id)
    self.id = d['id']
    self.name = d['name']
    self.type = d['type']
    self.price = d['price']
    self.quantity = d['quantity']
    self.expirydate = d['expirydate']
    self.facility = d['facility']
  
  def push(self):
    self.DB.update_item(self.id, self.name, self.type, self.price, self.quantity, self.expirydate, self.facility)
  
  def remove(self):
    self.DB.remove_item(self.id)



class StockManagement:
  def __init__(self, DB):
    self.DB = DB
    self.s = []
    self.pull()
  
  
  def pull(self):
    s = []
    for i in self.DB.get_items():
      s.append(Stock(self.DB, i['id'], i['name'], i['type'], i['price'], i['quantity'], i['expirydate'], i['facility']))
    self.s = s
    
  
  def add_item(self, name, type, price, quantity, expirydate, facility):
    self.s.append(Stock(self.DB, len(self.s), name, type, price, quantity, expirydate, facility, new=True))
  
  
  def get_item(self, id):
    for i in self.s:
      if i.id == id:
        return i
    raise Exception('Item not found')

  
  def get_items(self, sortby='id', sortdir='asc'):
    if sortby == 'id':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.id)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.id, reverse=True)
    elif sortby == 'name':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.name)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.name, reverse=True)
    elif sortby == 'type':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.type)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.type, reverse=True)
    elif sortby == 'price':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.price)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.price, reverse=True)
    elif sortby == 'quantity':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.quantity)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.quantity, reverse=True)
    elif sortby == 'expirydate':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.expirydate)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.expirydate, reverse=True)
    elif sortby == 'facility':
      if sortdir == 'asc':
        return sorted(self.s, key=lambda i: i.facility)
      elif sortdir == 'desc':
        return sorted(self.s, key=lambda i: i.facility, reverse=True)
    else:
      raise Exception('Invalid sortby')
  
  
  def edit_item(self, id, name, type, price, quantity, expirydate, facility):
    for i in self.s:
      if i.id == id:
        i.name = name
        i.type = type
        i.price = price
        i.quantity = quantity
        i.expirydate = expirydate
        i.facility = facility
        i.push()
        return
    raise Exception('Item not found')
  
  
  def remove_item(self, id):
    for i in self.s:
      if i.id == id:
        i.remove()
        self.s.remove(i)
        return
    raise Exception('Item not found')
