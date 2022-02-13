from pymongo import MongoClient


class MongoConnector:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__connection = None
        self.db = None
        self.collection = None

    def connect(self):
        if self.__connection:
            return
        self.__connection = MongoClient(self.host, self.port)
        self.db = self.__connection['test']
        self.collection = self.db['retail']

    def disconnect(self):
        if self.__connection:
            self.__connection.close()

    def insert_bulk_retails(self, data):
        if not self.__connection:
            self.connect()
        self.collection.insert_many(data)
