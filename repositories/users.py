import typing

from pymongo import MongoClient
import config

from models import User, Role
import dataclass_factory

from models.user import Warn


class UsersRepository:
    def __init__(self):
        self.db = MongoClient(config.config['mongo_url'])['bpl-admin']
        self.users = self.db["users"]
        self.factory = dataclass_factory.Factory()
        if not self.db.users.find_one({'role': 'owner'}):
            self.init_owners()

    def init_owners(self):
        for owner_id in config.OWNERS:
            self.create_user(owner_id, 'owner')

    @property
    def owners_ids(self) -> typing.List[int]:
        owners = self.get_users_by_role('owner')
        owners_ids = [owner.id for owner in owners]
        return owners_ids

    @property
    def owners(self) -> typing.List[User]:
        return self.get_users_by_role('owner')

    @property
    def admins(self) -> typing.List[User]:
        return self.get_users_by_role('admin')

    @property
    def admins_ids(self) -> typing.List[int]:
        admins = self.get_users_by_role('admin')
        return [admin.id for admin in admins]

    def is_user_admin(self, user_id: int) -> bool:
        return user_id in self.admins_ids+self.owners_ids

    def get_user(self, user_id: int) -> typing.Optional[User]:
        user = self.users.find_one({'id': user_id})
        if not user:
            return None
        return self.serialize_user(user)

    def get_user_or_insert(self, user_id: int) -> User:
        user = self.get_user(user_id)
        if not user:
            return self.create_user(user_id)
        return user

    def get_users_by_role(self, role: Role) -> typing.List[User]:
        users_dicts = self.users.find({'role': role})
        users = self.serialize_users(users_dicts)
        return users

    def serialize_user(self, user_dict: dict) -> User:
        return self.factory.load(user_dict, User)

    def serialize_users(self, users_dicts: list) -> typing.List[User]:
        return list(map(lambda user_dict: self.serialize_user(user_dict), users_dicts))

    def create_user(self, user_id: int, role: Role = 'user') -> User:
        user_dict = {
            'id': user_id,
            'role': role,
            'warns': [],
        }
        self.users.insert_one(user_dict)
        return self.serialize_user(user_dict)

    def warn_user(self, user_id: int, warn: Warn):
        dict = self.factory.dump(warn)
        self.users.update_one({'id': user_id}, {'$push': {'warns': dict}})

    def get_count_of_user_warns(self, user_id: int) -> typing.Optional[int]:
        user = self.get_user(user_id)
        if user is not None:
            return len(user.warns)

    def remove_warns(self, user_id: int):
        self.users.update_one({'id': user_id}, {'$set': {'warns': []}})
