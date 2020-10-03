# Всякая мелкая функциональность, которой не нашлось место в других папках
import typing

from telebot.types import PollOption


def parse_time_to_ban(args: str) -> typing.Optional[typing.Tuple[int, str]]:
    time = ""
    unit = ""
    it = iter(args)
    try:
        for char in it:
            if char.isdigit():
                time += char
            else:
                unit += char
                break
    except:
        return None
    try:
        for char in it:
            if not char.isspace():
                unit += char
            else:
                break
    except:
        return None

    if unit not in ["s", "m", "h", "d"]:
        return None

    return int(time), unit


def calculate_time_to_ban(time: int, unit: str) -> int:
    if unit == "s":
        return time
    elif unit == "m":
        return time * 60
    elif unit == "h":
        return time * 3600
    elif unit == "d":
        return time * 3600 * 24


def parse_and_calc_time_to_ban(args: str) -> typing.Optional[int]:
    res = parse_time_to_ban(args)
    if res is None:
        return None

    (time, unit) = res
    return calculate_time_to_ban(time, unit)


def get_max_poll_answer(answers: typing.List[PollOption]) -> typing.List[PollOption]:
    max_count = max(answer.voter_count for answer in answers)
    return list(filter(lambda a: a.voter_count == max_count, answers))
