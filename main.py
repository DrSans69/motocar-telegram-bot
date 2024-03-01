import re
import datetime
import os

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Chat
# import aiogram.utils.markdown as text_decorate

from src.parser import parse
from src.messages import get_messages
from src.templates import get_templates

dp = Dispatcher()
LOG_SPLITER = "-" * 20
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
MAX_MESSAGE_CHARS = 4096
messages = get_messages()
templates_base = get_templates()


with open("TOKEN", 'r') as f:
    TOKEN = f.read()


async def main() -> None:
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    print("Bot started")

    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    print(LOG_SPLITER)
    print("Start - id:{} - time:{}".format(
        message.from_user.id,
        get_current_time(message))
    )

    answer = messages['start']['en']
    answer = answer.replace('[!name]', message.from_user.full_name)
    await message.answer(answer)
    await help_message(message)


@dp.message(Command("help"))
async def command_help_handelr(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    print(LOG_SPLITER)
    print("Help - id:{} - time:{}".format(
        message.from_user.id,
        get_current_time(message))
    )

    await help_message(message)


@dp.message()
async def handler(message: Message) -> None:
    print(LOG_SPLITER)
    print("Msg - id:{} - time:{}".format(
        message.from_user.id,
        get_current_time(message))
    )

    text = message.text
    if not text:
        print("No text provided")
        await help_message(message)
        return

    print(text)

    olx_pattern = re.compile(r'(?:auto.ria.com/uk).+')
    links = olx_pattern.findall(text)

    if not links:
        print("No links provided")
        await help_message(message)
        return

    link = links[0]
    result = parse(r'https://' + link)

    if type(result) is not dict:
        print("Res in't dict")
        await help_message(message)
        return

    await make_ad(message, result)


async def make_ad(message: Message, result: dict) -> None:
    print("Result:")
    print(result)

    data = {
        '[!name]': result.get('name', 'N/A'),
        '[!price]': result.get('price', 'N/A'),
        '[!location]': result.get('location', 'N/A'),
        '[!mileage]': result.get('mileage', 'N/A'),
        '[!description]': result.get('description', 'N/A'),
        '[!drive]': result.get('params', {}).get('drive', 'N/A'),
        '[!engine]': result.get('params', {}).get('engine', 'N/A'),
        '[!transmission]': result.get('params', {}).get('transmission', 'N/A'),
        '[!phone]': result.get('phones', ['N/A'])[0],
        '[!phones]': '\n'.join([str(phone) for phone in result.get('phones', ['N/A'])]),
    }

    response = templates_base['default']

    for placeholder, value in data.items():
        response = response.replace(placeholder, str(value))

    await message.answer(response)

    print("Req sus - id:{} - time:{}".format(
        message.from_user.id,
        get_current_time())
    )


def get_current_time(message: Message = None) -> str:
    if message is None:
        return datetime.datetime.now(datetime.UTC).strftime(DATE_FORMAT)
    return message.date.strftime(DATE_FORMAT)


async def help_message(message: Message) -> None:
    await message.answer(messages['help']['en'])


if __name__ == "__main__":
    asyncio.run(main())
