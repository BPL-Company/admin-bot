import datetime
from dataclasses import dataclass

import models
from models.user import Warn
from repositories import UsersRepository
from services import TelebotService
import config
from services.polls import PollState, PollService
from utils import get_max_poll_answer
from views import messages
from views.text_messages import units


class UsersService:
    def __init__(self, users_repository: UsersRepository, telebot_service: TelebotService, poll_service: PollService):
        self.users_repository = users_repository
        self.telebot_service = telebot_service
        self.poll_service = poll_service
        self.states_poll_curt = []

    def ban_user(self, from_user: int, to_user: int, chat_id, time: int):
        if self.users_repository.is_user_admin(from_user):
            if self.users_repository.is_user_admin(to_user):
                return {'res': 'err', 'reason': 'target is admin'}

            self.telebot_service.ban_member(to_user, chat_id, time)
            return {'res': 'ok'}
        else:
            return {'res': 'err', 'reason': 'not an admin'}

    def mute_user(self, from_user: int, to_user: int, chat_id, time: int):
        if self.users_repository.is_user_admin(from_user):
            if self.users_repository.is_user_admin(to_user):
                return {'res': 'err', 'reason': 'target is admin'}

            self.telebot_service.restrict_member(to_user, chat_id, time)
            return {'res': 'ok'}
        else:
            return {'res': 'err', 'reason': 'not an admin'}

    def kick_user(self, from_user: int, to_user: int, chat_id):
        if self.users_repository.is_user_admin(from_user):
            if self.users_repository.is_user_admin(to_user):
                return {'res': 'err', 'reason': 'target is admin'}

            self.telebot_service.kick_member(to_user, chat_id)
            return {'res': 'ok'}
        else:
            return {'res': 'err', 'reason': 'not an admin'}

    def warn_user(self, from_user: int, to_user: int, reason: str, link: str):
        if self.users_repository.is_user_admin(from_user):
            if self.users_repository.is_user_admin(to_user):
                return {'res': 'err', 'reason': 'target is admin'}

            self.users_repository.warn_user(to_user, Warn(reason, link))
            now_warns = self.users_repository.get_count_of_user_warns(to_user)
            if now_warns >= config.MAX_WARNS:
                return {'res': 'ok', 'is_max_warns': True, 'warns': now_warns}

            return {'res': 'ok', 'is_max_warns': False, 'warns': now_warns}
        else:
            return {'res': 'err', 'reason': 'not an admin'}

    def clear_warns(self, from_user: int, to_user: int):
        if self.users_repository.is_user_admin(from_user):
            if self.users_repository.is_user_admin(to_user):
                return {'res': 'err', 'reason': 'target is admin'}

            self.users_repository.remove_warns(to_user)

            return {'res': 'ok'}
        else:
            return {'res': 'err', 'reason': 'not an admin'}

    def poll_curt_end(self, user_id: int, state: PollState):
        max_answers = get_max_poll_answer(state.poll.options)
        if len(max_answers) == 1:
            text = max_answers[0].text
            curt = StatePollCurt(user_id, state, text)
            self.states_poll_curt.append(curt)
            return {'res': 'ok', 'curt': curt}
        else:
            return {'res': 'err', 'variants': list(map(lambda m: m.text, max_answers))}

    def administrator_confirm_curt(self, user_id: int):
        states = list(filter(lambda state: state.user_id == user_id, self.states_poll_curt))
        if len(states) == 0:
            return {'res': 'err', 'reason': 'no curt on that users'}
        else:
            curt: StatePollCurt = states[0]
            state = curt.poll_state
            action = curt.action
            if action == "Помиловать":
                self.users_repository.remove_warns(user_id)
                self.telebot_service.send_message(
                    state.message.chat.id,
                    messages['have mercy'].format(user_id, "этого чувака")
                )
            elif action == "Бан на день":
                self.telebot_service.ban_member(
                    user_id,
                    state.message.chat.id,
                    (datetime.datetime.now() + datetime.timedelta(1)).timestamp()
                )
                self.telebot_service.send_message(
                    state.message.chat.id,
                    messages['banned at time'].format(user_id, "Этот чувак", 1, units['d'])
                )
            elif action == "Бан на неделю":
                self.telebot_service.ban_member(
                    user_id,
                    state.message.chat.id,
                    (datetime.datetime.now() + datetime.timedelta(7)).timestamp()
                )
                self.telebot_service.send_message(
                    state.message.chat.id,
                    messages['banned at time'].format(user_id, "Этот чувак", 7, units['d'])
                )
            elif action == "Бан навсегда!":
                self.telebot_service.ban_member(
                    user_id,
                    state.message.chat.id,
                    datetime.datetime.now().timestamp()
                )
                self.telebot_service.send_message(
                    state.message.chat.id,
                    messages['banned forever'].format(user_id, "Этот чувак", "навсегда", "")
                )
            elif action == "Отобрать козу.":
                pass
            else:
                pass
            return {'res': 'ok'}

    def administrator_not_confirm_curt(self, user_id: int, admin_id: int):
        states = list(filter(lambda state: state.user_id == user_id, self.states_poll_curt))
        if len(states) == 0:
            return {'res': 'err', 'reason': 'no curt on that users'}
        else:
            curt: StatePollCurt = states[0]
            self.states_poll_curt.pop(self.states_poll_curt.index(states[0]))
            self.telebot_service.send_message(
                curt.poll_state.message.chat.id,
                messages['administrator not confirm curt'].format(admin_id, curt.action)
            )
            return {'res': 'ok'}

    def create_user_if_need(self, user_id: int):
        self.users_repository.get_user_or_insert(user_id)

    def get_user(self, id: int) -> models.User:
        return self.users_repository.get_user(id)


@dataclass
class StatePollCurt:
    user_id: int
    poll_state: PollState
    action: str
