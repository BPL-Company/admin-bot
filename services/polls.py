import typing
from threading import Timer

from telebot.types import Poll, Message

from services import TelebotService


class PollService:
    def __init__(self, telebot_service: TelebotService):
        self.polls: typing.List[PollState] = []
        self.telebot_service = telebot_service

    def create_poll(
            self,
            chat_id: int,
            question: str,
            answers: typing.List[str],
            time: float,
            on_end: typing.Callable[['PollState'], None]
    ):
        poll = self.telebot_service.start_poll(chat_id, question, answers)
        self.polls.append(PollState(poll, poll.poll, time, on_end))

    def update_poll(self, poll: Poll):
        poll_state = self.find_poll(poll.id)
        if poll_state is not None:
            poll_state.poll = poll

    def find_poll(self, id: str) -> typing.Optional['PollState']:
        for poll_state in self.polls:
            if poll_state.poll.id == id:
                return poll_state


class PollState:
    def __init__(self, message: Message, poll: Poll, time: float, on_end: typing.Callable[['PollState'], None]):
        self.message = message
        self.poll = poll
        self.thread = Timer(time, lambda: on_end(self))
        self.thread.start()
