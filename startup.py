from bot import bot
from repositories import UsersRepository
from services import TelebotService, UsersService
from services.polls import PollService

users_repo = UsersRepository()
telebot_service = TelebotService(bot)
poll_service = PollService(telebot_service)
users_service = UsersService(users_repo, telebot_service, poll_service)
