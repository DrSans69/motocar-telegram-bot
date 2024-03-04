import os
import json
import re

from src.consts import *


def check_user_data(id: str) -> dict:
    dir_path = user_dir(id)

    if os.path.exists(dir_path):
        return get_user_data(id)

    os.makedirs(dir_path)
    os.mkdir(os.path.join(dir_path, 'templates'))

    with open(os.path.join(dir_path, 'user_data.json'), 'w') as f:
        json.dump(BASE_USER_DATA, f)

    return get_user_data(id)


def get_user_data(id: str) -> dict:
    filename = os.path.join(user_dir(id), 'user_data.json')

    with open(filename, 'r') as f:
        return json.load(f)


def get_user_templates(id: str) -> list:
    templates_dir = os.path.join(user_dir(id), 'templates')
    if not os.path.exists(templates_dir):
        os.mkdir(templates_dir)

    templates = os.listdir(templates_dir)
    for i, template in enumerate(templates):
        if template[-4:] == '.txt':
            templates[i] = template[:-4]

    return templates


def is_valid_filename(filename: str, id: str) -> bool:
    if not len(filename) or len(filename) > MAX_TEMPLATE_NAME_LENGTH:
        return False

    if filename.endswith(' ') or filename.endswith('.'):
        return False

    basename = filename.upper().split('.')[0]
    if basename in RESERVED_NAMES_WINDOWS:
        return False

    if filename in get_user_templates(id):
        return False

    if filename in base_templates:
        return False

    for c in filename:
        if c not in ALLOWED_CHARS_FOR_TEMPLATE_NAME:
            return False

    return True


def user_dir(id: str) -> str:
    id = id_to_str(id)
    return os.path.join('tmp', 'users', id)


def save_template(id: str | int, filename: str, template: str) -> bool:
    try:
        dir_path = os.path.join(user_dir(id), 'templates')
        with open(os.path.join(dir_path, filename + '.txt'), 'w') as f:
            f.write(template)
        return True
    except:
        return False


def id_to_str(id: str | int) -> str:
    if type(id) is str:
        id = int(id)
    return str(id)


def get_template_text(filename: str, id: str) -> tuple[str, str]:
    filename += '.txt'
    template = os.path.join(user_dir(id), 'templates', filename)
    if os.path.exists(template):
        with open(template, 'r') as f:
            return f.read(), 'u'

    template = os.path.join('templates', filename)
    if os.path.exists(template):
        with open(template, 'r') as f:
            return f.read(), 'b'
    return None, None


def delete_template(filename: str, id: str) -> None:
    filename += '.txt'
    template = os.path.join(user_dir(id), 'templates', filename)
    os.remove(template)


def make_default_template(template: str, id: str) -> None:
    filename = os.path.join(user_dir(id), 'user_data.json')

    with open(filename, 'r') as file:
        data = json.load(file)

    data['template'] = template

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file)
