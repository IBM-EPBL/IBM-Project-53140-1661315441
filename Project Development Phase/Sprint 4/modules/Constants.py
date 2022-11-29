class Constants:
    def __init__(self):
        self.SORTBY = ('id', 'name', 'type', 'price', 'quantity', 'facility')
        self.USERPRIVILEGES = {'superadmin': -1,
                               'admin': 0, 'user': 1, 'visitor': 2}
        self.CATEGORIES = ('uncategorised', 'grocery', 'snack',
                           'homeappliance', 'stationary', 'electronics', 'other')
