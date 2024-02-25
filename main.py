import asyncio
import re
from src.parser import parse
import datetime

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
    print(
        f"Start message - id:{message.from_user.id} - time:{get_current_time(message)}")
    """
    This handler receives messages with `/start` command
    """
    s = []
    s.append(f"Hello, <b><i>{message.from_user.full_name}</i></b>!")
    await message.answer("\n".join(s))
    await command_help_handelr(message)


@dp.message(Command("help"))
async def command_help_handelr(message: Message) -> None:
    print(
        f"Help message - id:{message.from_user.id} - time:{get_current_time(message)}")
    """
    This handler receives messages with `/help` command
    """
    s = []
    s.append(
        f"I will parse the offer from auto ria and create a telegram message from it"
    )
    s.append(f"Give me a link to try")
    await message.answer("\n".join(s))


@dp.message()
async def handler(message: Message) -> None:
    print(
        f"Request message - id:{message.from_user.id} - time:{get_current_time(message)}")

    text = message.text
    if not text:
        print("No text provided")
        await command_help_handelr(message)

    print('Message:')
    print(text)

    olx_pattern = re.compile(r'(?:auto.ria.com/uk).+')
    links = olx_pattern.findall(text)

    if not links:
        print("No links provided")
        await command_help_handelr(message)
        return

    link = links[0]
    try:
        result = parse(r'https://' + link)
        if type(result) is not dict:
            await command_help_handelr(message)
        await make_ad(message, result)
    except ImportError:
        print("Error while tring to make ad")
        await command_help_handelr(message)


async def make_ad(message: Message, result: dict) -> None:
    print("Result:")
    print(result)

    name = result.get('name', 'N/A')
    price = result.get('price', 'N/A')
    location = result.get('location', 'N/A')
    mileage = result.get('mileage', 'N/A')
    phones = result.get('phones', [])

    description = result.get('description', 'N/A')
    description = description.replace('<br>', '\n')
    description = description.replace('</br>', '\n')
    description = description.replace('<br/>', '\n')
    params = result.get('params', {})
    drive = params.get('drive', 'N/A')
    engine = params.get('engine', 'N/A')
    transmission = params.get('transmission', 'N/A')

    # Construct the response message
    response_message = ""
    response_message += f"🚗{name}\n"
    response_message += f"💸{price}\n"
    response_message += f"✈️{location}\n"
    response_message += f"🛣{mileage} тис. км\n\n"

    response_message += "📱Власник:\n"
    for phone in phones:
        response_message += phone

    response_message += "\n\n\nХарактеристики:\n\n"
    response_message += f"⚙️Привід: {drive}\n"
    response_message += f"⚙️Двигун: {engine}\n"
    response_message += f"⚙️Коробка передач: {transmission}\n\n"

    response_message += "!?Короткий опис\n"
    response_message += description

    response_message += "\n\nСлава Україні !🇺🇦"

    # Send the message back to the user
    await message.answer(response_message)

    print(
        f"Request complete - id:{message.from_user.id} - time:{get_current_time()}")


def get_current_time(message: Message = None):
    if message is None:
        return datetime.datetime.now(datetime.UTC).strftime('%d-%m-%Y %H:%M:%S')
    return message.date.strftime('%d-%m-%Y %H:%M:%S')


if __name__ == "__main__":
    asyncio.run(main())
