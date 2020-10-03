from dataclasses import dataclass

import typing


class Roles:
    Admin = "admin"
    User = "user"
    Owner = "owner"


Role = typing.Union[Roles.User, Roles.Admin, Roles.Owner]


@dataclass
class Warn:
    reason: str
    link: str


@dataclass
class User:
    id: int
    role: str
    warns: typing.List[Warn]
