from models import User, Warn


def view_warn_limit(user: User) -> str:
    text = f"О нет! <a href='tg://user?id={user.id}'>Товарищ</a> первысил количество допустимых предупреждений. Что " \
           f"мы сделаем с ним за это? Вот его проступки:\n"
    text += "\n".join(map(show_warn, user.warns))
    return text


def show_warn(warn: Warn) -> str:
    return f"<a href='{warn.link}'>{warn.reason if warn.reason != '' else 'Предупреждение'}</a>"


WARN_ACTIONS = ["Помиловать", "Бан на день", "Бан на неделю", "Бан навсегда!", "Отобрать козу."]
