from threading import Thread
import time


class Stock:
    def __init__(self, DB, id, name, type, price, quantity, minvalue, facility, new=False):
        self.DB = DB
        self.id = str(id)
        self.name = str(name)
        self.type = str(type)
        self.price = str(price)
        self.quantity = str(quantity)
        self.minvalue = str(minvalue)
        self.facility = str(facility)
        if new:
            self.id = str(self.DB.add_item(
                self.name, self.type, self.price, self.quantity, self.minvalue, self.facility))

    def pull(self):
        d = self.DB.get_item(self.id)
        self.id = d['id']
        self.name = d['name']
        self.type = d['type']
        self.price = d['price']
        self.quantity = d['quantity']
        self.minvalue = d['minvalue']
        self.facility = d['facility']

    def push(self):
        self.DB.update_item(self.id, self.name, self.type,
                            self.price, self.quantity, self.minvalue, self.facility)

    def remove(self):
        self.DB.remove_item(self.id)


class StockManagement:
    def __init__(self, DB, UM, FM, SG):
        self.DB = DB
        self.UM = UM
        self.FM = FM
        self.SG = SG
        self.s = []
        self.pull()
        self.send_minlist_email()

    def pull(self):
        s = []
        for i in self.DB.get_items():
            s.append(Stock(self.DB, i['id'], i['name'], i['type'],
                     i['price'], i['quantity'], i['minvalue'], i['facility']))
        self.s = s

    def add_item(self, name, type, price, quantity, minvalue, facility):
        i = Stock(self.DB, len(self.s), name, type, price,
                  quantity, minvalue, facility, new=True)
        self.s.append(i)
        self.DB.add_log(facility, i.id, price, quantity, 'added')

    def get_item(self, id):
        for i in self.s:
            if int(i.id) == int(id):
                return i
        return Stock(self.DB, 'NOT FOUND', 'NOT FOUND', 'NOT FOUND', 'NOT FOUND', 'NOT FOUND', 'NOT FOUND', 'NOT FOUND')

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
        elif sortby == 'facility':
            if sortdir == 'asc':
                return sorted(self.s, key=lambda i: i.facility)
            elif sortdir == 'desc':
                return sorted(self.s, key=lambda i: i.facility, reverse=True)
        else:
            raise Exception('Invalid sortby')

    def edit_item(self, id, name, type, price, quantity, minvalue, facility):
        for i in self.s:
            if i.id == id:
                oldquantity = int(i.quantity)
                if name:
                    i.name = name
                if type:
                    i.type = type
                if price:
                    i.price = price
                if quantity:
                    i.quantity = quantity
                if minvalue:
                    i.minvalue = minvalue
                if facility:
                    i.facility = facility
                i.push()
                quantity = int(quantity)
                if oldquantity < quantity:
                    self.DB.add_log(facility, i.id, price, quantity - oldquantity,
                                    'added' if self.FM.get_facility(i.facility).type == 'store' else 'received')
                elif oldquantity > quantity:

                    self.DB.add_log(facility, i.id, price, oldquantity - quantity,
                                    'sold' if self.FM.get_facility(i.facility).type == 'store' else 'sent')
                return
        raise Exception('Item not found')

    def edit_quantity(self, id, quantity):
        for i in self.s:
            if i.id == id:
                oldquantity = int(i.quantity)
                i.quantity = quantity
                quantity = int(quantity)
                i.push()
                if oldquantity < quantity:
                    self.DB.add_log(i.facility, i.id, i.price, quantity - oldquantity,
                                    'added' if self.FM.get_facility(i.facility).type == 'store' else 'received')
                elif oldquantity > quantity:
                    self.DB.add_log(i.facility, i.id, i.price, oldquantity - quantity,
                                    'sold' if self.FM.get_facility(i.facility).type == 'store' else 'sent')
                return
        raise Exception('Item not found')

    def remove_item(self, id):
        for i in self.s:
            if i.id == id:
                i.remove()
                self.s.remove(i)
                return
        raise Exception('Item not found')

    def get_minlist(self):
        minlist = []
        for i in self.s:
            if int(i.quantity) <= int(i.minvalue):
                minlist.append(i)
        return minlist

    def send_minlist_email(self):
        self.t = Thread(target=self.minlist_thread)
        self.t.start()

    def minlist_thread(self):
        while True:
            minlist = self.get_minlist()
            if len(minlist) > 0:
                msg = 'The following items are below minimum value:\n' + \
                    '\n'.join([i.name for i in minlist])
                for i in self.UM.get_users():
                    if i.privilege() < 1:
                        a = self.SG.send(
                            i.email, 'Smart Stock - Low Stock Notification', msg)
            time.sleep(7200)
