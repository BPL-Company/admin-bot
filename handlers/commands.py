from telebot.types import Message

from .actions import banmute_user, kick_user
from .validators import validate_usage_of_banmute_command, validate_usage_of_kick_command

from bot import bot
from startup import telebot_service, users_service
from views import messages


@bot.message_handler(commands=["ban"], content_types=["text"])
def handle_ban_command(message: Message):
    res = validate_usage_of_banmute_command(message)()

    if res is None:
        return

    banmute_user(
        res,
        message,
        users_service.ban_member,
        messages["successful ban by reason"],
        messages["successful ban"]
    )()


@bot.message_handler(commands=["mute"], content_types=["text"])
def handle_mute_command(message: Message):
    res = validate_usage_of_banmute_command(message)()

    if res is None:
        return

    banmute_user(
        res,
        message,
        users_service.mute_user,
        messages["successful mute by reason"],
        messages["successful mute"]
    )()


@bot.message_handler(commands=["kick"], content_types=["text"])
def handle_kick_command(message: Message):
    reason = validate_usage_of_kick_command(message)()

    if reason is None:
        return

    kick_user(
        reason,
        message,
        users_service.kick_user,
        messages["successful kick by reason"],
        messages["successful kick"]
    )()
