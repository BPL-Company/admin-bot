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
        return self.greet_sessions.get(user_id)

    def greet_user(self, user_id, bot) -> dict:
        if user_id in self.greeted_users:
            return {'text': messages['greeting']}
        session = self.form_session()
        session.create_member(user_id)
        session.inject_callback_handler(bot, messages['antispam'])
        self.greet_sessions.update({
            user_id: session
        })
        self.greeted_users.add(user_id)
        return {
            'text': messages['antispam'],
            'reply_markup': session.get_tg_map('0_0')
        }

    def form_session(self) -> World:
        session = World()
        session.walk_attention = messages['antispam_too_far']
        session.look_range = 3
        session.spawns = ['0_0']

        @session.create_tile()
        def nothing_handler(member, pos):
            pass

        @session.create_tile(name='goat', icon='🐐', destructuble=True)
        def wall_handler(member, pos):
            return messages['antispam_goat']

        session.insert_map({
            random.choice(session.get_visible_tiles('0_0')): 'goat'
        })
        return session


greeter = Greeter()
