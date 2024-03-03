from aiogram.types import Message, CallbackQuery
import datetime
from src.consts import *


def get_current_time(val: Message | CallbackQuery = None) -> str:
    if type(val) is not Message:
        return datetime.datetime.now(datetime.UTC).strftime(DATE_FORMAT)
    return val.date.strftime(DATE_FORMAT)


def log_message(key_word: str, val: CallbackQuery | Message, spliter=True) -> None:
    if spliter:
        print(LOG_SPLITER)
    print("{} - id:{} - time:{}".format(
        key_word,
        val.from_user.id,
        get_current_time(val))
    )
