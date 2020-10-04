from views.text_messages import messages
from models import User


def view_show_user(user: User) -> str:
    return messages["show user"].format(
        user.id,
        user.role,
        user.warns.count()
    )
