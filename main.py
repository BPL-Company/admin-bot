from bot import bot

from handlers import *


def start_polling():
    print("started polling")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    start_polling()
