import typing
import dataclass_factory

from pymongo import MongoClient

import config
from models import Curt


class CurtsRepository:
    def __init__(self):
        self.db = MongoClient(config.config['mongo_url'])['bpl-admin']
        self.curts = self.db["users"]
        self.factory = dataclass_factory.Factory()
    
    def add_curt(self, curt: Curt):
        deserialized = self.factory.dump(curt)
        self.curts.insert_one(deserialized)
    
    def user_curts(self, user_id: int):
        curts = self.curts.find({"user_id" : {"$eq" : user_id}})
        return curts
