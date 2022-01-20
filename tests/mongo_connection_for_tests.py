from connection import MongoConnection


class MongoConnectionForTest(MongoConnection):

    def __init__(self):
        super().__init__()

    def get_collection(self):
        return self.db.get_collection('tests')