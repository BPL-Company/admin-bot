import typing

from telebot.types import Message

from startup import telebot_service
from utils import calculate_time_to_ban
from views import messages
from views.text_messages import units


def banmute_user(
        options: typing.Tuple[int, str, str],
        m: Message,
        on_ban: typing.Callable[[int, int, int, int], typing.Dict[str, str]],
        message_when_reason_exists: str,
        message_when_reason_does_not_exists: str,
) -> typing.Callable[[], None]:
    (time, unit, reason) = options

    time_to_ban = calculate_time_to_ban(time, unit)
    res = on_ban(m.from_user.id, m.reply_to_message.from_user.id, m.chat.id, time_to_ban)
    if res["res"] == "err":
        return lambda: telebot_service.send_message(m.chat.id, messages[res["reason"]])
    else:
        if reason != "":
            text = message_when_reason_exists.format(
                m.from_user.id,
                m.from_user.first_name,
                m.reply_to_message.from_user.id,
                m.reply_to_message.from_user.first_name,
                time,
                units[unit],
                reason,
            )
        else:
            text = message_when_reason_does_not_exists.format(
                m.from_user.id,
                m.from_user.first_name,
                m.reply_to_message.from_user.id,
                m.reply_to_message.from_user.first_name,
                time,
                units[unit],
            )
        return lambda: telebot_service.send_message(m.chat.id, text)
