import typing
from telebot.types import Message

from utils import parse_time_to_ban
from startup import telebot_service
from views import messages


def validate_usage_of_reply_command(m: Message) -> typing.Callable[[], bool]:
    if not m.reply_to_message:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])


def validate_usage_of_banmute_command(m: Message) -> typing.Callable[[], typing.Optional[typing.Tuple[int, str, str]]]:
    text: list = m.text.split(maxsplit=2)
    if len(text) == 1:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])

    res = parse_time_to_ban(text[1])
    if res is None:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])

    if not m.reply_to_message:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])

    return lambda: res
