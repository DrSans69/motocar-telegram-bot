import os


def get_templates(dir: str = 'templates'):
    commands = {}
    for filename in os.listdir(os.path.join(dir)):
        with open(os.path.join(dir, filename), 'r') as f:
            commands[filename.replace('.txt', '')] = f.read()
    return commands


def get_messages(dir: str = 'messages'):
    commands = {}
    for subdir in os.listdir(dir):
        commands[subdir] = {}
        for filename in os.listdir(os.path.join(dir, subdir)):
            with open(os.path.join(dir, subdir, filename), 'r') as f:
                commands[subdir][filename.replace('.txt', '')] = f.read()
    return commands


def get_buttons(dir: str = 'buttons'):
    commands = {}
    for subdir in os.listdir(dir):
        commands[subdir] = {}
        for filename in os.listdir(os.path.join(dir, subdir)):
            with open(os.path.join(dir, subdir, filename), 'r') as f:
                commands[subdir][filename.replace('.txt', '')] = f.read()
    return commands
