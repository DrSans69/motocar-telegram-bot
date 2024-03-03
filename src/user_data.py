import os
import json

from src.consts import *


def check_user_data(id: str | int) -> dict:
    dir_path = user_dir(id)

    if os.path.exists(dir_path):
        return get_user_data(id)

    os.makedirs(dir_path)
    os.mkdir(os.path.join(dir_path, 'templates'))

    with open(os.path.join(dir_path, 'user_data.json'), 'w') as f:
        json.dump(BASE_USER_DATA, f)

    return get_user_data(id)


def get_user_data(id: str | int) -> dict:
    filename = os.path.join(user_dir(id), 'user_data.json')

    with open(filename, 'r') as f:
        return json.load(f)


def get_user_templates(id: str | int) -> list:
    templates_dir = os.path.join(user_dir(id), 'templates')
    if not os.path.exists(templates_dir):
        os.mkdir(templates_dir)

    return os.listdir(templates_dir)


def user_dir(id: str | int) -> str:
    if type(id) is str:
        id = int(id)
    id = str(id)

    return os.path.join('tmp', 'users', id)
