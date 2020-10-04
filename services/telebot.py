import typing
from telebot import TeleBot
from telebot.types import Message


class TelebotService:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def ban_member(self, user_id: int, chat_id: int, time: int):
        self.bot.kick_chat_member(chat_id, user_id, until_date=time)

    def restrict_member(self, user_id: int, chat_id: int, time: int):
        self.bot.restrict_chat_member(chat_id, user_id, until_date=time)

    def kick_member(self, user_id: int, chat_id: int):
        self.bot.unban_chat_member(chat_id, user_id)

    def send_message(self, chat_id: int, text: str, *args, reply_markup=None):
        self.bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode="HTML")

    def start_poll(self, chat_id: int, question: str, options: typing.List[str]) -> Message:
        return self.bot.send_poll(chat_id, question, options)

    def delete_message(self, chat_id: int, message_id: int):
        self.bot.delete_message(chat_id, message_id)

    def answer_callback_query(self, query_id: int, text: str = None):
        self.bot.answer_callback_query(query_id, text)

    def unban_user(self, chat_id: int, user_id: int):
        self.bot.unban_chat_member(chat_id, user_id)

    def unmute_user(self, chat_id: int, user_id: int):
        self.bot.restrict_chat_member(
            chat_id,
            user_id,
            None,
            True,
            True,
            True,
            True,
            True
        )
