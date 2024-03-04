from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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

    user_data = get_user_data(message.from_user.id)
    print(user_data)
    template = user_data.get('template', 'default')

    response, _ = get_template_text(template, message.from_user.id)
    print(response)

    if response is None:
        response, _ = get_template_text('default', message.from_user.id)

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


async def create_template_message(val: Message | CallbackQuery, state: FSMContext):
    user_data = get_user_data(val.from_user.id)
    lang = user_data.get('lang', 'en')

    await state.set_data({'template': ''})

    fields = list(get_data_from_result({}).keys())

    response = messages['create_template'][lang]
    response = response.replace('[!fields]', '\n'.join(fields))

    if type(val) is Message:
        await val.answer(response, disable_web_page_preview=True)
    elif type(val) is CallbackQuery:
        await val.message.answer(response, disable_web_page_preview=True)


async def name_template_message(message: Message, state: FSMContext):
    user_data = get_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    data = await state.get_data()
    data['template_name'] = ''
    await state.set_data(data)

    response = messages['name_template'][lang]
    response = response.replace(
        '[!chars]', ' '.join(ALLOWED_CHARS_FOR_TEMPLATE_NAME))
    response = response.replace(
        '[!len]', str(MAX_TEMPLATE_NAME_LENGTH))

    await message.answer(response)


async def show_template_message(val: CallbackQuery, filename: str):
    if not filename:
        return

    user_data = get_user_data(val.from_user.id)
    lang = user_data.get('language', 'en')

    template, template_type = get_template_text(
        filename, val.from_user.id)
    if template is None:
        return

    kb = [[
        InlineKeyboardButton(
            text=buttons['make_default_template'][lang],
            callback_data='mdt_' + filename),
    ]]

    if template_type == 'u':
        kb[0].append(
            InlineKeyboardButton(
                text=buttons['delete_template'][lang],
                callback_data='dlt_' + filename)
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await val.message.answer(template, reply_markup=keyboard, disable_web_page_preview=True)
    await val.answer()
