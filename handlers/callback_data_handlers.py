import logging

from telebot import types

from bot import bot
from startup import users_service, telebot_service
from views import messages
from views.text_messages import units


@bot.callback_query_handler(func=lambda data: data.data.startswith('curt'))
def handle_curt_buttons(c: types.CallbackQuery):
    logging.debug(f'Receive curt administrator answer: "{c.data}"')
    res = c.data.split('|')
    if len(res) != 3:
        telebot_service.answer_callback_query('Что-то пошло не так')
        print(f"Error! Curt button send data: '{c.data}'")
        return
    user_id = int(res[2])
    if res[1] == "confirm":
        res = users_service.administrator_confirm_curt(user_id)
    elif res[1] == "not confirm":
        res = users_service.administrator_not_confirm_curt(user_id, c.from_user.id)
    if res['res'] == 'ok':
        telebot_service.delete_message(c.message.chat.id, c.message.message_id)
        if res['action'] == 'have mercy':
            telebot_service.send_message(
                res['state'].message.chat.id,
                messages['have mercy'].format(user_id, "этого чувака")
            )
        elif res['action'] == 'ban':
            if res['time'] == 'forever':
                telebot_service.send_message(
                    res['state'].message.chat.id,
                    messages['banned forever'].format(user_id, "Этот чувак")
                )
            else:
                telebot_service.send_message(
                    res['state'].message.chat.id,
                    messages['banned at time'].format(user_id, "Этот чувак", res['time'], units[res['unit']])
                )
    else:
        telebot_service.answer_callback_query(c.id, messages[res['reason']])


@bot.callback_query_handler(func=lambda _: True)
def show_queries(c: types.CallbackQuery):
    print(f"New query: '{c.data}'")
