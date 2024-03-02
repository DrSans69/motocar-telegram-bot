import re
import datetime
import os
import json
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, Chat, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

# import aiogram.utils.markdown as text_decorate

from src.parser import parse
from src.messages import get_messages
from src.templates import get_templates
from src.buttons import get_buttons

LOG_SPLITER = "-" * 20
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
MAX_MESSAGE_CHARS = 4096
BASE_LANGUAGE = 'en'
INLINE_TEMPLATES_NUMBER = 6
BASE_USER_DATA = {
    "language": "en",
    "templates": "dafault"
}

dp = Dispatcher()
messages = get_messages()
base_templates = get_templates()
buttons = get_buttons()


with open("TOKEN", 'r') as f:
    TOKEN = f.read()


async def main() -> None:
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    print("Bot started")

    await dp.start_polling(bot)


@dp.message(Command("test"))
async def test(message: Message):
    log_message("Templates", message)
    user_data = check_user_data(message.from_user.id)


@dp.message(Command("templates"))
async def command_templates_handler(message: Message):
    log_message("Templates", message)
    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')
    user_templates = get_user_templates(message.from_user.id)

    kb = [[
        InlineKeyboardButton(
            text=buttons['add_template'][lang],
            callback_data='create_template')
    ]]

    for template in user_templates:
        kb.append([
            InlineKeyboardButton(
                text=template,
                callback_data='shw_u_' + template)
        ])

    for template in base_templates.keys():
        kb.append([
            InlineKeyboardButton(
                text=template,
                callback_data='shw_u_' + template)
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(messages['templates'][user_data['language']], reply_markup=keyboard)


@dp.callback_query(F.data == "create_template")
async def callback_create_template(callback: CallbackQuery):
    log_message("Make template", callback)

    await callback.message.edit_reply_markup(reply_markup=None)
    await create_template_handler(callback)


async def create_template_handler(callback: CallbackQuery):
    message = callback.message
    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    await callback.message.answer(messages['create_template'][lang])


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    log_message("Start", message)

    answer = messages['start']['en']
    answer = answer.replace('[!name]', message.from_user.full_name)

    await message.answer(answer)
    await help_message(message)


@dp.message(Command("help"))
async def command_help_handelr(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    log_message("Help", message)
    await help_message(message)


@dp.message()
async def handler(message: Message) -> None:
    log_message("Msg", message)

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

    response = base_templates['default']

    for placeholder, value in data.items():
        response = response.replace(placeholder, str(value))

    await message.answer(response, disable_web_page_preview=True)

    print("{} - id:{} - time:{}".format(
        "Req sus",
        message.from_user.id,
        get_current_time())
    )


async def help_message(message: Message) -> None:
    await message.answer(messages['help']['en'])


def get_current_time(val: Message | CallbackQuery = None) -> str:
    if val is None or type(val) is not Message:
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


def check_user_data(id: str | int) -> dict:
    dir_path = user_dir(id)

    if os.path.exists(dir_path):
        return get_user_data(id)

    os.makedirs(dir_path)
    os.mkdir(os.path.join(dir_path, 'templates'))

    with open(os.path.join(dir_path, 'user_data.json'), 'w') as f:
        json.dump(BASE_USER_DATA, f)

    return get_user_data(id)


def get_user_data(id: str | int) -> dict:
    filename = os.path.join(user_dir(id), 'user_data.json')

    with open(filename, 'r') as f:
        return json.load(f)


def get_user_templates(id: str | int) -> list:
    templates_dir = os.path.join(user_dir(id), 'templates')
    if not os.path.exists(templates_dir):
        os.mkdir(templates_dir)

    return os.listdir(templates_dir)


def user_dir(id: str | int) -> str:
    if type(id) is str:
        id = int(id)
    id = str(id)

    return os.path.join('tmp', 'users', id)


if __name__ == "__main__":
    asyncio.run(main())
