import random
import typing
from sdtg import World
from views.text_messages import messages


class Greeter:
    def __init__(self):
        self.greeted_users = set()
        self.greet_sessions = dict()

    def is_user_greeted(self, user_id) -> bool:
        return user_id in self.greeted_users

    def get_greet_session(self, user_id) -> typing.Optional[typing.Tuple[int]]:
        return self.greet_sessions.get(user_id)['session']

    def greet_user(self, user_id, chat_id, bot) -> dict:
        if user_id in self.greeted_users:
            return {'text': messages['greeting']}
        session = self.create_session(bot, chat_id, user_id)
        session.create_member(user_id)
        session.inject_callback_handler(bot, messages['antispam'])
        self.greet_sessions.update({
            user_id: {
                'session': session,
                'chat_id': chat_id
            }
        })
        self.greeted_users.add(user_id)
        return {
            'text': messages['antispam'],
            'reply_markup': session.get_tg_map('0_0')
        }

    def create_session(self, bot, chat_id, user_id) -> World:
        session = World()
        session.walk_attention = messages['antispam_too_far']
        session.walk_range = 1
        session.look_range = 3
        session.spawns = ['0_0']

        @session.create_tile()
        def nothing_handler(member, pos):
            pass

        @session.create_tile(name='goat', icon='🐐', destructuble=True)
        def wall_handler(member, pos):
            bot.send_message(chat_id, 'Испытание козой пройдено!')
            bot.restrict_chat_member(chat_id, user_id, None, True, True, True, True, True)
            return messages['antispam_goat']

        session.insert_map({
            random.choice(session.get_visible_tiles('0_0')): 'goat'
        })
        return session

    def fail(self, bot, user_id, chat_id, message_id):
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, 'Испытание козой провалено!')
        bot.unban_chat_member(chat_id, user_id)

