from models import User


class UsersRepository:
    def add_user(self, user: User):
        pass

    def is_user_admin(self, user_id: int) -> bool:
        pass
