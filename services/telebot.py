from telebot import TeleBot


class TelebotService:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def ban_member(self, user_id: int, chat_id: int, time: int):
        self.bot.kick_chat_member(chat_id, user_id, until_date=time)

    def restrict_member(self, user_id: int, chat_id: int, time: int):
        self.bot.restrict_chat_member(chat_id, user_id, until_date=time)

    def kick_member(self, user_id: int, chat_id: int):
        self.bot.unban_chat_member(chat_id, user_id)

    def send_message(self, chat_id: int, text: str):
        self.bot.send_message(chat_id, text, parse_mode="HTML")
