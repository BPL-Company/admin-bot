from bot import bot

from repositories import UsersRepository
from services import TelebotService, UsersService

users_repo = UsersRepository()  # TODO: add pymongo
telebot_service = TelebotService(bot)
users_service = UsersService(users_repo, telebot_service)

import handlers


def start_polling():
    print("started polling")
    bot.polling(none_stop=True)


start_polling()
