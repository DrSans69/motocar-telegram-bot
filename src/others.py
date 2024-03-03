import re
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.consts import *
from src.logs import *
from src.user_data import *
from pprint import pprint


async def make_ad(message: Message, result: dict) -> None:
    print("Result:")
    pprint(result)

    data = get_data_from_result(result)

    response = base_templates['default']

    for placeholder, value in data.items():
        response = response.replace(placeholder, str(value))

    await message.answer(response, disable_web_page_preview=True)

    print("{} - id:{} - time:{}".format(
        "Req sus",
        message.from_user.id,
        get_current_time())
    )


def get_data_from_result(result: dict) -> dict:
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
    return data


async def help_message(message: Message) -> None:
    await message.answer(messages['help']['en'])


async def create_template_message(message: Message, state: FSMContext):
    user_data = get_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    await state.set_data({'template': ''})

    fields = list(get_data_from_result({}).keys())

    response = messages['create_template'][lang]
    response = response.replace('[!fields]', '\n'.join(fields))

    await message.answer(response)


async def name_template_message(message: Message, state: FSMContext):
    user_data = get_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    data = await state.get_data()
    data['template_name'] = ''
    await state.set_data(data)

    await message.answer(messages['name_template'][lang])


def is_valid_filename(filename: str) -> bool:
    if not len(filename) or re.search(r'[<>:"/\\|?*\0\n\r\t]', filename):
        return False

    if filename.endswith(' ') or filename.endswith('.'):
        return False

    basename = filename.upper().split('.')[0]
    if basename in RESERVED_NAMES_WINDOWS:
        return False

    return True
