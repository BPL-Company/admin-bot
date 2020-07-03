from telebot.types import Message, Poll

from bot import bot
from startup import users_service, poll_service


@bot.message_handler(content_types=["text"])
def handle_text_message(message: Message):
    users_service.create_user_if_need(message.from_user.id)


@bot.poll_handler(lambda _: True)
def handle_polls(poll: Poll):
    poll_service.update_poll(poll)
