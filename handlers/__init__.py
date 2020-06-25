from telebot.types import Message
from utils import parse_time_to_ban, calculate_time_to_ban

from bot import bot
from main import telebot_service, users_service
from views import messages
from views.text_messages import units


@bot.message_handler(commands=["ban"], content_types=["text"])
def handle_ban_command(m: Message):
    print(1)
    text: list = m.text.split(maxsplit=2)
    if len(text) == 1:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return

    res = parse_time_to_ban(text[1])
    if res is None:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return

    (time, unit, reason) = res
    time = calculate_time_to_ban(time, unit)

    if not m.reply_to_message:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return
    res = users_service.ban_user(m.from_user.id, m.reply_to_message.from_user.id, m.chat.id, time)
    if res["res"] == "err":
        telebot_service.send_message(m.chat.id, messages[res["reason"]])
    else:
        if reason != "":
            text = messages["successful ban by reason"].format(
                m.from_user.first_name,
                m.from_user.id,
                m.reply_to_message.from_user.first_name,
                m.reply_to_message.from_user.id,
                time,
                units[unit],
                reason,
            )
        else:
            text = messages["successful ban"].format(
                m.from_user.first_name,
                m.from_user.id,
                m.reply_to_message.from_user.first_name,
                m.reply_to_message.from_user.id,
                time,
                units[unit],
            )
        telebot_service.send_message(m.chat.id, text)


@bot.message_handler(content_types=["text"])
def t(m):
    print(m)


print("handlers loaded")
