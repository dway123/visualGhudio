import configparser
from pymongo import MongoClient

CONFIG_NAME = "config.txt"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_NAME)

        # Parse and connect to database
        uri = config['mongodb.com']['ConnectionString']
        db_name = config['mongodb.com']['DbName']
        collection_name = config['mongodb.com']['CollectionName']
        client = MongoClient(uri)
        db = client[db_name]
        self.collection = db[collection_name]

    def insert(self, key, value):
        post = {key : value}
        post_id = self.collection.insert_one(post).inserted_id

# # Test
# database = Database()
# database.insert('sure', 'I can');
