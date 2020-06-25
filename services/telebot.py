from telebot import TeleBot


class TelebotService:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def ban_member(self, user_id: int, chat_id: int, time: int):
        self.bot.kick_chat_member(chat_id, user_id, until_date=time)

    def restrict_member(self, user_id: int, chat_id: int, time: int):
        self.bot.restrict_chat_member(chat_id, user_id, until_date=time)

    def send_message(self, chat_id: int, text: str):
        self.bot.send_message(chat_id, text, parse_mode="HTML")

    def is_user_admin(self, chat_id: int, user_id: int):
        admins = self.bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in admins)
