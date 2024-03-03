from aiogram.types import Message
from src.consts import *
from src.logs import *
from src.user_data import *
from pprint import pprint


async def make_ad(message: Message, result: dict) -> None:
    print("Result:")
    pprint(result)

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


async def create_template_handler(callback: CallbackQuery):
    message = callback.message
    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    await callback.message.answer(messages['create_template'][lang])
