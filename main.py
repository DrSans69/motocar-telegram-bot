import asyncio
import re
import subprocess

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Chat
# import aiogram.utils.markdown as text_decorate

PARSER = "parser.js"
with open("TOKEN", "r") as f:
    TOKEN = f.read()


dp = Dispatcher()


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
    s = []
    s.append(f"Hello, <b><i>{message.from_user.full_name}</i></b>!")
    await message.answer("\n".join(s))
    await command_help_handelr(message)


@dp.message(Command("help"))
async def command_help_handelr(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    s = []
    s.append(
        f"I will parse the offer from auto ria and create a telegram message from it")
    s.append(f"Give me a link to try")
    await message.answer("\n".join(s))


@dp.message()
async def handler(message: Message) -> None:
    text = message.text
    if not text:
        await command_help_handelr(message)

    olx_pattern = re.compile(r'(?:auto.ria.com/uk).+')
    links = olx_pattern.findall(text)

    if links:
        for link in links:
            result = parser(link)
            print(str(result))
    else:
        await command_help_handelr(message)


async def parser(link: str):
    subprocess.run(["node", PARSER, link])


if __name__ == "__main__":
    asyncio.run(main())
