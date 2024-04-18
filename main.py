import re
import asyncio
from pprint import pprint

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from src.scraper import *
from src.import_data import *
from src.consts import *
from src.logs import *
from src.user_data import *
from src.others import *

dp = Dispatcher()


class User(StatesGroup):
    default = State()
    creating_template = State()
    naming_template = State()


async def main() -> None:
    global bot
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    print("Bot started")

    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    log_message("Start", message)

    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    answer = messages['start'][lang]
    answer = answer.replace('[!name]', message.from_user.full_name)

    await message.answer(answer)
    await help_message(message)


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
                callback_data='ts_' + template)
        ])

    for template in base_templates:
        kb.append([
            InlineKeyboardButton(
                text=template,
                callback_data='ts_' + template)
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(messages['templates'][user_data['language']], reply_markup=keyboard)


@dp.message(Command("help"))
async def command_help_handelr(message: Message) -> None:
    log_message("Help", message)
    await help_message(message)


@dp.message(Command("settings"))
async def command_help_handelr(message: Message) -> None:
    log_message("Setting", message)

    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    await message.answer(messages['settings'][lang])


@dp.message(User.creating_template)
async def creating_template_handler(message: Message, state: FSMContext) -> None:
    log_message("Create template", message)
    print(message.text)

    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    if message.text.lower() == 'quit':
        await state.set_state(User.default)
        await message.answer(messages['quit'][lang])
        return

    elif message.text.lower() == 'no' or message.text.lower() == 'n':
        await create_template_message(message, state)
        return

    elif message.text.lower() == 'yes' or message.text.lower() == 'y':
        await state.set_state(User.naming_template)
        await name_template_message(message, state)
        return

    await state.set_data({'template': message.text})

    await message.answer(messages['confirm'][lang])


@dp.message(User.naming_template)
async def naming_template_handler(message: Message, state: FSMContext):
    log_message("Name template", message)
    print(message.text)

    user_data = check_user_data(message.from_user.id)
    lang = user_data.get('lang', 'en')

    if message.text.lower() == 'quit':
        await state.set_state(User.default)
        await message.answer(messages['quit'][lang])
        return

    elif message.text.lower() == 'no' or message.text.lower() == 'n':
        await name_template_message(message, state)
        return

    elif message.text.lower() == 'yes' or message.text.lower() == 'y':
        log_message("Template created", message)
        data = await state.get_data()
        pprint(data)
        if is_valid_filename(data['template_name'], message.from_user.id):
            await state.set_state(User.default)
            if save_template(message.from_user.id,
                             data['template_name'], data['template']):
                await message.answer(messages['template_created'][lang])
            else:
                await message.answer(messages['error'][lang])
        else:
            await message.answer(messages['invalid_template_name'][lang])
        return

    if is_valid_filename(message.text, message.from_user.id):
        data = await state.get_data()
        data['template_name'] = message.text
        await state.set_data(data)
    else:
        await message.answer(messages['invalid_template_name'][lang])
        return

    await message.answer(messages['confirm'][lang])


@dp.message()  # must be at the end #todo: fix
async def default_handler(message: Message) -> None:
    log_message("Msg", message)

    check_user_data(message.from_user.id)

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
    result = scrape(r'https://' + link)

    if type(result) is not dict:
        print("Res in't dict")
        await help_message(message)
        return

    await make_ad(message, result)

# commands


@dp.callback_query(F.data == "create_template")
async def callback_create_template(callback: CallbackQuery, state: FSMContext):
    log_message("Make template", callback)

    await state.set_state(User.creating_template)

    await callback.message.edit_reply_markup(reply_markup=None)
    await create_template_message(callback, state)


@dp.callback_query(F.data.startswith('ts_'))
async def callback_show_user_templat(callback: CallbackQuery):
    log_message("Show template", callback)

    await show_template_message(
        callback, callback.data.replace('ts_', '', 1))
    await callback.answer()


@dp.callback_query(F.data.startswith('dlt_'))
async def callback_show_user_templat(callback: CallbackQuery):
    log_message("Delete template", callback)

    user_data = get_user_data(callback.from_user.id)
    lang = user_data.get('language', 'en')

    delete_template(
        callback.data.replace('dlt_', '', 1), callback.from_user.id)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(messages['delete_template'][lang])


@dp.callback_query(F.data.startswith('mdt_'))
async def callback_show_user_templat(callback: CallbackQuery):
    log_message("Make default template", callback)

    user_data = get_user_data(callback.from_user.id)
    lang = user_data.get('language', 'en')

    make_default_template(
        callback.data.replace('mdt_', '', 1), callback.from_user.id)

    await callback.answer(messages['make_default_template'][lang])


# callbacks

if __name__ == "__main__":
    asyncio.run(main())
