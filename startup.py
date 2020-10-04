from bot import bot
from repositories import UsersRepository, CurtsRepository
from services import TelebotService, UsersService, Greeter
from services.polls import PollService

users_repo = UsersRepository()
curts_repo = CurtsRepository()
telebot_service = TelebotService(bot)
poll_service = PollService(telebot_service)
users_service = UsersService(users_repo, telebot_service, poll_service, curts_repo)
greeter = Greeter()
