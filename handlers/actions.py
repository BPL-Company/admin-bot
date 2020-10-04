import typing

from telebot import types
from telebot.types import Message

import config
from services.polls import PollState
from services.users import StatePollCurt
from startup import telebot_service, users_service, poll_service, users_repo
from utils import calculate_time_to_ban
from views import messages
from views.text_messages import units
from views.warn_views import view_warn_limit
from views.users import view_show_user
from models import User


def banmute_user(
        options: typing.Tuple[int, str, str],
        m: Message,
        on_ban: typing.Callable[[int, int, int, int], typing.Dict[str, str]],
        message_when_reason_exists: str,
        message_when_reason_does_not_exists: str,
):
    (time, unit, reason) = options

    time_to_ban = calculate_time_to_ban(time, unit)
    res = on_ban(m.from_user.id, m.reply_to_message.from_user.id, m.chat.id, m.date + time_to_ban)
    if res["res"] == "err":
        telebot_service.send_message(m.chat.id, messages[res["reason"]])
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
        telebot_service.send_message(m.chat.id, text)


def kick_user(
        reason: str,
        m: Message,
        on_kick: typing.Callable[[int, int, int], typing.Dict[str, str]],
        message_when_reason_exists: str,
        message_when_reason_does_not_exists: str,
):

    res = on_kick(m.from_user.id, m.reply_to_message.from_user.id, m.chat.id)
    if res["res"] == "err":
        telebot_service.send_message(m.chat.id, messages[res["reason"]])
    else:
        if reason != "":
            text = message_when_reason_exists.format(
                m.from_user.id,
                m.from_user.first_name,
                m.reply_to_message.from_user.id,
                m.reply_to_message.from_user.first_name,
                reason,
            )
        else:
            text = message_when_reason_does_not_exists.format(
                m.from_user.id,
                m.from_user.first_name,
                m.reply_to_message.from_user.id,
                m.reply_to_message.from_user.first_name,
            )
        telebot_service.send_message(m.chat.id, text)


def warn_user(
        reason: str,
        m: Message,
):
    if m.chat.username:
        link = f"t.me/{m.chat.username}/{m.message_id}"
    else:
        link = f"t.me/{m.chat.id}/{m.message_id}"
    res = users_service.warn_user(m.from_user.id, m.reply_to_message.from_user.id, reason, link)
    if res["res"] == "err":
        telebot_service.send_message(m.chat.id, messages[res["reason"]])
        return
    else:
        if res["is_max_warns"]:
            user = users_repo.get_user(m.reply_to_message.from_user.id)
            telebot_service.send_message(m.chat.id, view_warn_limit(user))
            poll_service.create_poll(
                m.chat.id,
                messages["what do with person?"],
                ["Помиловать", "Бан на день", "Бан на неделю", "Бан навсегда!"],
                config.TIME_POLL_WARN,
                lambda state: on_curt_end(m.reply_to_message.from_user.id, state)
            )
        else:
            telebot_service.send_message(
                m.chat.id,
                messages["new warn"].format(
                    m.reply_to_message.from_user.id,
                    m.reply_to_message.from_user.first_name,
                    res["warns"]
                )
            )


def on_curt_end(user_id: int, state: PollState):
    res = users_service.poll_curt_end(user_id, state)
    if res['res'] == 'ok':
        curt: StatePollCurt = res['curt']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(messages['confirm'], callback_data=f"curt|confirm|{user_id}"))
        markup.add(types.InlineKeyboardButton(messages['not confirm'], callback_data=f"curt|not confirm|{user_id}"))
        telebot_service.send_message(
            state.message.chat.id,
            messages['wait admin confirm curt'].format(curt.action, user_id, "этого человека"),
            reply_markup=markup
        )
    else:
        telebot_service.send_message(state.message.chat.id, messages["yet curt poll"])
        poll_service.create_poll(
            state.message.chat.id,
            "Что делать с товарищем?",
            res['variants'],
            config.TIME_POLL_WARN,
            lambda state: on_curt_end(user_id, state)
        )


def clear_warns(
        m: Message,
):
    res = users_service.clear_warns(m.from_user.id, m.reply_to_message.from_user.id)
    if res["res"] == "err":
        telebot_service.send_message(m.chat.id, messages[res["reason"]])
    else:
        telebot_service.send_message(m.chat.id, messages["clear warns"].format(
            m.reply_to_message.from_user.id,
            m.reply_to_message.from_user.first_name
        ))

def show_user(m: Message):
    user: User = users_repo.get_user(m.from_user.id)
    text = view_show_user(user)
    telebot_service.send_message(m.chat.id, text)
