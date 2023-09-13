import configparser
import os
import time

path = 'config.cfg'

def create_config():
    config = configparser.ConfigParser()
    config.add_section("Settings")


    with open(path, "w",encoding='utf-8') as config_file:
        config.write(config_file)


def check_config_file():
    if not os.path.exists(path):
        create_config()

        print('Config created')
        time.sleep(3)
        exit(0)


def config(what):
    config = configparser.ConfigParser()
    config.read(path,'utf-8')

    value = config.get("Settings", what)

    return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path,'utf-8')

    config.set("Settings", setting, value)

    with open(path, "w",encoding='utf-8') as config_file:
        config.write(config_file)


check_config_file()
