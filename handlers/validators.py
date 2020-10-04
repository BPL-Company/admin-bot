import typing
from telebot.types import Message

from utils import parse_time_to_ban
from startup import telebot_service
from views import messages


def validate_usage_of_kick_command(m: Message) -> typing.Optional[str]:
    if not m.reply_to_message:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return None
    else:
        text = m.text.split(maxsplit=1)
        if len(text) == 1:
            return ""
        else:
            return text[1]


def validate_usage_of_warn_command(m: Message) -> typing.Optional[str]:
    if not m.reply_to_message:
        return telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
    else:
        text = m.text.split(maxsplit=1)
        if len(text) == 1:
            return ""
        else:
            return text[1]


def validate_usage_of_banmute_command(m: Message) -> typing.Optional[typing.Tuple[int, str, str]]:
    text: list = m.text.split(maxsplit=2)
    if len(text) == 1:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return None

    if len(text) == 3:
        reason = text[2]
    else:
        reason = ""

    res = parse_time_to_ban(text[1])
    if res is None:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return None

    if not m.reply_to_message:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return None

    return res[0], res[1], reason


def validate_usage_of_removable_command(m: Message) -> bool:
    if not m.reply_to_message:
        telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
        return False
    else:
        return True
