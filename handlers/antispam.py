from threading import Timer

from telebot.types import Message

from bot import bot
from startup import users_repo, greeter


@bot.message_handler(content_types=['new_chat_members'])
def new_users_handler(m: Message):
    for tg_user in m.new_chat_members:
        user = users_repo.get_user_or_insert(tg_user.id)
        bot.restrict_chat_member(m.chat.id, user.id, None, False)
        kwargs = greeter.greet_user(user.id, m.chat.id, bot)
        message_id = bot.reply_to(m, kwargs['text'], reply_markup=kwargs['reply_markup'])
        kick_timer = Timer(300, greeter.fail, args=[bot, m.chat.id, user.id, message_id])

