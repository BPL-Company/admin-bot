from .commands import handle_ban_command, handle_kick_command, handle_mute_command

from .antispam import *

from .text_handlers import handle_text_message
from .callback_data_handlers import handle_curt_buttons, show_queries


print("handlers loaded")
