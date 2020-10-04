from models.user import Roles

messages = {
    "wrong usage of command": "Неправильное использование команды!",
    "not an admin": "Вы не администратор!",
    "target is admin": "Вы не можете совершить это действие с администратором.",
    "successful ban": "<a href='tg://user?id={}'>{}</a> забанил <a href='tg://user?id={}'>{}</a> на {} {}!",
    "successful ban by reason":
        "<a href='tg://user?id={}'>{}</a> забанил <a href='tg://user?id={}'>{}</a> на {} {} по причине {}!",
    "successful mute": "<a href='tg://user?id={}'>{}</a> заглушил <a href='tg://user?id={}'>{}</a> на {} {}!",
    "successful mute by reason":
        "<a href='tg://user?id={}'>{}</a> заглушил <a href='tg://user?id={}'>{}</a> на {} {} по причине {}!",
    "successful kick": "<a href='tg://user?id={}'>{}</a> кикнул <a href='tg://user?id={}'>{}</a>!",
    "successful kick by reason":
        "<a href='tg://user?id={}'>{}</a> кикнул <a href='tg://user?id={}'>{}</a> по причине {}!",
    "have mercy": "Вы решили помиловать <a href='tg://user?id={}'>{}</a>! У него смылись предупреждения.",
    "new warn": "<a href='tg://user?id={}'>{}</a> получил предупреждение! В сумме у него {} предупреждений.",
    "yet curt poll": "Вы набрали одинаковое количество голосов по нескольким пунктам. назначаю переголосование!",
    "what do with person?": "Что делать с товарищем?",
    "banned at time": "<a href='tg://user?id={}'>{}</a> бал забанен на {} {}",
    "banned forever": "<a href='tg://user?id={}'>{}</a> бал забанен навсегда",
    "clear warns": "Вы помыли пользователя <a href='tg://user?id={}'>{}</a>!",
    "confirm": "Подтвердить",
    "not confirm": "Не подтвердить",
    "wait admin confirm curt": "Подождите, пока администратор утвердит приговор <i>{}</i> для <a href='tg://user?id={"
                               "}'>{}</a> ",
    "no curt on that users": "Нет опросов с этим пользователем",
    "administrator not confirm curt": "<a href='tg://user?id={}'>Администратор</a> не подтвердил выбранную меру "
                                      "пресечения \"{}\"! ",
    "show user": 
        "id: {}\n"
        "Роль: {}\n"
        "Варны: {}\n"
}

units = {
    "h": "часов",
    "m": "минут",
    "s": "секунд",
    "d": "дней",
}

roles = {
    Roles.Owner: "Владелец",
    Roles.Admin: "Админ",
    Roles.User: "Пользователь"
}
