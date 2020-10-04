from threading import Thread

from telebot.types import Message

from bot import bot
from startup import users_repo, greeter


@bot.message_handler(content_types=['new_chat_members'])
def new_users_handler(m: Message):
    for tg_user in m.new_chat_members:
        user = users_repo.get_user_or_insert(tg_user.id)
        kwargs = greeter.greet_user(user.id, bot)
        Thread(target=bot.reply_to, args=[m], kwargs=kwargs).start()
