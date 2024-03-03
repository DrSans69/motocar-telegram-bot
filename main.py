import re
import datetime
import os
import json
import asyncio
import pprint

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.parser import *
from src.import_data import *
from src.consts import *
from src.logs import *
from src.user_data import *
from src.others import *

dp = Dispatcher()


async def main() -> None:
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    print("Bot started")

    await dp.start_polling(bot)


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


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    log_message("Start", message)

    answer = messages['start']['en']
    answer = answer.replace('[!name]', message.from_user.full_name)

    await message.answer(answer)
    await help_message(message)


@dp.message(Command("help"))
async def command_help_handelr(message: Message) -> None:
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

# commands


@dp.callback_query(F.data == "create_template")
async def callback_create_template(callback: CallbackQuery):
    log_message("Make template", callback)

    await callback.message.edit_reply_markup(reply_markup=None)
    await create_template_handler(callback)

# callbacks

if __name__ == "__main__":
    asyncio.run(main())
