from dataclasses import dataclass

import typing


class Roles:
    Admin = "admin"
    User = "user"


Role = typing.Union[Roles.User, Roles.Admin]


@dataclass
class User:
    username: str
    id: int
    role: Role
