import json
class StockItem:
    def __init__(self, item, stock):
        self.item = item
        self.stock = stock

    def to_dict(self):
        return json.dumps(self.__dict__, indent=2) + ','

    def to_csv(self):
        return ','.join([str(f) for f in self.__dict__.values()]) + '\n'
