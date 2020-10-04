# TODO: здесь будут сервисы.
# В сервисах происходит вся бизнес логика. Они вызываются из хендлеров, проводят некоторые операции,
# работают с репозиториями и другими сервисами. Возвращают результат работы в виде объекта/словаря.

from .telebot import TelebotService
from .users import UsersService
from .greeter import Greeter
