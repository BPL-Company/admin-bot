from repositories import UsersRepository
from services import TelebotService


class UsersService:
    def __init__(self, users_repository: UsersRepository, telebot_service: TelebotService):
        self.users_repository = users_repository
        self.telebot_service = telebot_service

    def ban_user(self, from_user: int, to_user: int, chat_id, time: int):
        if self.users_repository.is_user_admin(from_user):
            self.telebot_service.ban_member(to_user, chat_id, time)
            return {'res': 'ok'}
        else:
            return {'res': 'err', 'reason': 'not an admin'}

    def mute_user(self, from_user: int, to_user: int, chat_id, time: int):
        if self.users_repository.is_user_admin(from_user):
            self.telebot_service.restrict_member(to_user, chat_id, time)
            return {'res': 'ok'}
        else:
            return {'res': 'err', 'reason': 'not an admin'}
