class LogManagement:
    def __init__(self, DB, SM):
        self.DB = DB
        self.SM = SM

    def add_log(self, facility, item, price, quantity, action):
        self.DB.add_log(facility, item, price, quantity, action)

    def get_top_sold(self, limit):
        l = []
        for i in self.DB.get_top_sold(limit):
            i['name'] = self.SM.get_item(i['item']).name
            l.append(i)
        return l

    def get_today_logs(self):
        l = []
        for i in self.DB.get_today_logs():
            i['name'] = self.SM.get_item(i['item']).name
            l.append(i)
        return l

    def clear_all_logs(self):
        self.DB.clear_all_logs()
