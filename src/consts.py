from src.import_data import *

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

messages = get_messages()
buttons = get_buttons()
base_templates = get_templates()
