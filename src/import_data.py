import os


def get_templates(dir: str = 'templates') -> list:
    templates = os.listdir(dir)
    for i, template in enumerate(templates):
        if template[-4:] == '.txt':
            templates[i] = template[:-4]

    return templates


def get_messages(dir: str = 'messages'):
    commands = {}
    for subdir in os.listdir(dir):
        commands[subdir] = {}
        for filename in os.listdir(os.path.join(dir, subdir)):
            with open(os.path.join(dir, subdir, filename), 'r', encoding='utf8') as f:
                commands[subdir][filename.replace('.txt', '')] = f.read()
    return commands


def get_buttons(dir: str = 'buttons'):
    commands = {}
    for subdir in os.listdir(dir):
        commands[subdir] = {}
        for filename in os.listdir(os.path.join(dir, subdir)):
            with open(os.path.join(dir, subdir, filename), 'r', encoding='utf8') as f:
                commands[subdir][filename.replace('.txt', '')] = f.read()
    return commands
