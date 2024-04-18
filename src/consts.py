from src.import_data import *
from dotenv import load_dotenv

load_dotenv()

LOG_SPLITER = "-" * 20
DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
MAX_MESSAGE_CHARS = 4096
BASE_LANGUAGE = 'en'
INLINE_TEMPLATES_NUMBER = 6
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_USER_DATA = {
    "language": "en",
    "template": "dafault"
}
RESERVED_NAMES_WINDOWS = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
]
ALLOWED_CHARS_FOR_TEMPLATE_NAME = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', '_', '-', '0', '1',
    '2', '3', '4', '5', '6', '7', '8', '9'
]
MAX_TEMPLATE_NAME_LENGTH = 64 - 8

TECH_INFO_TABLE = {
    'Двигун': 'engine',
    'Привід': 'drive',
    'Коробка передач': 'transmission'
}

messages = get_messages()
buttons = get_buttons()
base_templates = get_templates()
