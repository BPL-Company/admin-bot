import logging

from telebot import types

from bot import bot
from startup import users_service, telebot_service
from views import messages


@bot.callback_query_handler(func=lambda data: data.data.startswith('curt'))
def handle_curt_buttons(c: types.CallbackQuery):
    logging.debug(f'Receive curt administrator answer: "{c.data}"')
    res = c.data.split('|')
    if len(res) != 3:
        telebot_service.answer_callback_query('Что-то пошло не так')
        print(f"Error! Curt button send data: '{c.data}'")
        return
    if res[1] == "confirm":
        res = users_service.administrator_confirm_curt(int(res[2]))
    elif res[1] == "not confirm":
        res = users_service.administrator_not_confirm_curt(int(res[2]), c.from_user.id)
    if res['res'] == 'ok':
        telebot_service.delete_message(c.message.chat.id, c.message.message_id)
    else:
        telebot_service.answer_callback_query(c.id, messages[res['reason']])


@bot.callback_query_handler(func=lambda _: True)
def show_queries(c: types.CallbackQuery):
    print(f"New query: '{c.data}'")
