from telebot.types import Message

from .actions import banmute_user, kick_user, warn_user, clear_warns, show_user
from .validators import validate_usage_of_banmute_command, validate_usage_of_kick_command, \
    validate_usage_of_warn_command

from bot import bot
from startup import users_service
from views import messages


@bot.message_handler(commands=["ban"], content_types=["text"])
def handle_ban_command(message: Message):
    users_service.create_user_if_need(message.from_user.id)
    res = validate_usage_of_banmute_command(message)

    if res is None:
        return

    banmute_user(
        res,
        message,
        users_service.ban_user,
        messages["successful ban by reason"],
        messages["successful ban"]
    )


@bot.message_handler(commands=["mute"], content_types=["text"])
def handle_mute_command(message: Message):
    users_service.create_user_if_need(message.from_user.id)
    res = validate_usage_of_banmute_command(message)

    if res is None:
        return

    banmute_user(
        res,
        message,
        users_service.mute_user,
        messages["successful mute by reason"],
        messages["successful mute"]
    )


@bot.message_handler(commands=["kick"], content_types=["text"])
def handle_kick_command(message: Message):
    users_service.create_user_if_need(message.from_user.id)
    reason = validate_usage_of_kick_command(message)

    if reason is None:
        return

    kick_user(
        reason,
        message,
        users_service.kick_user,
        messages["successful kick by reason"],
        messages["successful kick"]
    )


@bot.message_handler(commands=["warn"], content_types=["text"])
def handle_warn_command(message: Message):
    users_service.create_user_if_need(message.from_user.id)
    reason = validate_usage_of_warn_command(message)
    users_service.create_user_if_need(message.reply_to_message.from_user.id)

    if reason is None:
        return

    warn_user(reason, message)


@bot.message_handler(commands=["clear_warns"], content_types=["text"])
def handle_clear_warns_command(message: Message):
    users_service.create_user_if_need(message.from_user.id)
    users_service.create_user_if_need(message.reply_to_message.from_user.id)

    clear_warns(message)


@bot.message_handler(commands=["show_me"], content_types=["text"])
def handle_show_me_command(message: Message):
    users_service.create_user_if_need(message.from_user.id)
    
    show_user(message)
