class Facility:
  def __init__(self, DB, id, name, type, address, email, phone, new=False):
    self.DB = DB
    self.id = str(id)
    self.name = str(name)
    self.type = str(type)
    self.address = str(address)
    self.email = str(email)
    self.phone = str(phone)
    if new:
      self.id = str(self.DB.add_facility(self.name, self.type, self.address, self.email, self.phone))
  
  def pull(self):
    d = self.DB.get_facility(self.id)
    self.id = d['id']
    self.name = d['name']
    self.type = d['type']
    self.address = d['address']
    self.email = d['email']
    self.phone = d['phone']
  
  def push(self):
    self.DB.update_facility(self.id, self.name, self.type, self.address, self.email, self.phone)
  
  def remove(self):
    self.DB.remove_facility(self.id)



class FacilityManagement:
  def __init__(self, DB):
    self.DB = DB
    self.f = []
    self.pull()
  
  
  def pull(self):
    f = []
    for i in self.DB.get_facilities():
      f.append(Facility(self.DB, i['id'], i['name'], i['type'], i['address'], i['email'], i['phone']))
    self.f = f
  
  
  def add_facility(self, name, type, address, email, phone):
    self.f.append(Facility(self.DB, '-1', name, type, address, email, phone, new=True))
  
  
  def get_facility(self, id):
    for i in self.f:
      print(type(i.id), type(id))
      if i.id == id:
        return i
    raise Exception('Facility not found')
  
  
  def get_facilities(self):
    return self.f
  
  
  def edit_facility(self, id, name, type, address, email, phone):
    for i in self.f:
      if i.id == id:
        if name: i.name = name
        if type: i.type = type
        if address: i.address = address
        if email: i.email = email
        if phone: i.phone = phone
        i.push()
        return
    raise Exception('Facility not found')
  
  
  def remove_facility(self, id):
    for i in self.f:
      if i.id == id:
        self.f.remove(i)
        i.remove()
        return
    raise Exception('Facility not found')
  