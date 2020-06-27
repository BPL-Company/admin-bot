import typing
from telebot.types import Message

from utils import parse_time_to_ban
from startup import telebot_service
from views import messages


def validate_usage_of_kick_command(m: Message) -> typing.Callable[[], typing.Union[str, None]]:
    if not m.reply_to_message:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])
    else:
        text = m.text.split(maxsplit=1)
        if len(text) == 1:
            return lambda: ""
        else:
            return lambda: text[1]


def validate_usage_of_banmute_command(m: Message) -> typing.Callable[[], typing.Optional[typing.Tuple[int, str, str]]]:
    text: list = m.text.split(maxsplit=2)
    if len(text) == 1:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])

    if len(text) == 3:
        reason = text[2]
    else:
        reason = ""

    res = parse_time_to_ban(text[1])
    if res is None:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])

    if not m.reply_to_message:
        return lambda: telebot_service.send_message(m.chat.id, messages["wrong usage of command"])

    return lambda: (res[0], res[1], reason)
