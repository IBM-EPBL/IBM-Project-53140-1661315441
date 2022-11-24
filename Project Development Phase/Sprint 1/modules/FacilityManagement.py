class Facility:
  def __init__(self, DB, id, name, type, address, email, phone, new=False):
    self.DB = DB
    self.id = id
    self.name = name
    self.type = type
    self.address = address
    self.email = email
    self.phone = phone
    if new:
      self.DB.add_facility(self.id, self.name, self.type, self.address, self.email, self.phone)
  
  def pull(self):
    d = self.DB.get_facility(self.id)
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
    self.f.append(Facility(self.DB, len(self.f), name, type, address, email, phone, new=True))
  
  
  def get_facility(self, id):
    for i in self.f:
      if i.id == id:
        return i
    raise Exception('Facility not found')
  
  
  def get_facilities(self):
    return self.f
  
  