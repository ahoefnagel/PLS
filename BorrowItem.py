from datetime import datetime

class BorrowItem:
    def __init__(self, item, user):
        self.item = item
        self.user = user
        self.borrow_date = datetime.now()
        self.return_date = None

    def to_msv(self):
        return ' - '.join([str(f) for f in self.__dict__.values()]) + '\n'
