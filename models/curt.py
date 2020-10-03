from dataclasses import dataclass

import datetime
import typing

@dataclass
class Curt:
    user_id : int
    time: datetime.datetime
    message_id: int
    reason: str
    action: str
