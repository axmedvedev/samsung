from pymongo import MongoClient
from config import *

class MongoDB(object):
    def __init__(self, **kwarg):
        collection, config = list(map(lambda x: x[1], kwarg.items()))
        db_name, host, port, user, pwd = list(map(lambda x: x[1], config.items()))
        try:
            self._client = MongoClient(f'mongodb://{user}:{pwd}@{host}:{port}')
            self._collection = self._client[db_name][collection]
        except Exception as e:
            logging.error(f"[con] - {e}")

    def get_all(self):
        try:
            data = self._collection.find()
            result = []
            for item in data:
                result.append(item)
            return result
        except Exception as e:
            logging.error(f"[all] - {e}")
            return []
        finally:
            self._client.close()

    def get_one(self, target_key, target_value):
        try:
            data = self._collection.find_one({f"{target_key}": target_value})
            return data
        except Exception as e:
            logging.error(f"[one] - {e}")
            return []
        finally:
            self._client.close()
        
    def join(self, pipeline):
        try:
            result = self._collection.aggregate(pipeline)
            return list(result)
        except Exception as e:
            logging.error(f"[join] - {e}")
        finally:
            self._client.close()