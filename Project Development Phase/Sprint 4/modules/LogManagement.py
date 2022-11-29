class LogManagement:
  def __init__(self, DB, SM):
    self.DB = DB
    self.SM = SM
  
  def add_log(self, facility, item, price, quantity, action):
    print(f'LM.add_log: facility:{facility}, item:{item}, price:{price}, quantity:{quantity}, action:{action}')
    self.DB.add_log(facility, item, price, quantity, action)
  
  def get_top_sold(self, limit):
    print(f'LM.get_top_sold: limit:{limit}')
    l = []
    for i in self.DB.get_top_sold(limit):
      i['name'] = self.SM.get_item(i['item']).name
      l.append(i)
    print(l)
    return l

  def get_today_logs(self):
    print('LM.get_today_logs')
    l = []
    for i in self.DB.get_today_logs():
        i['name'] = self.SM.get_item(i['item']).name
        l.append(i)
    print(l)
    return l
  
  def clear_all_logs(self):
    print('LM.clear_all_logs')
    self.DB.clear_all_logs()
  