# -*- coding: utf-8 -*-
import sqlite3
import telebot
import os
import random
import requests
import json
import datetime
import threading
import traceback
import config

from time import time
from datetime import datetime, date
from sys import exit
from random import choice
from telebot import types
from logger import *


admin_sending_messages_dict = {}

class Admin_sending_messages:
    def __init__(self, user_id):
        self.user_id = user_id
        self.text = None
        self.photo = None
        self.type_sending = None
        self.date = None


def first_join(user_id, username):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    ref_code = 0
    if ref_code == '':
        ref_code = 0
    
    if len(row) == 0:
        users = [f"{user_id}", f"{username}", f"{date.today()}", "0", "0", "0", "0", "0", "0", "0", "0"]
        cursor.execute(f'INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)', users)
        conn.commit()

        return True, ref_code
        
    return False, 0

def check_user_in_bd(user_id):

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    check = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    if len(check) > 0:
        return True
    else:
        return False

def profile(user_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

    return row


def users_info():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users').fetchone()

    current_time = str(datetime.now())

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    while row is not None:
        amount_user_all += 1
        if row[2][:-15:] == current_time[:-15:]:
            amount_user_day += 1
        if row[2][:-13:] == current_time[:-13:]:
            amount_user_hour += 1

        row = cursor.fetchone()

    msg = f"""
🏃‍♂️<b>Старт бота</b>: <code>2020-12-12</code>
👥 <b>Пользователей</b>: <code>{amount_user_all}</code>
"""

    return msg

def admin_info():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users').fetchone()

    current_time = str(datetime.now())

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    while row is not None:
        amount_user_all += 1
        if row[2][:-15:] == current_time[:-15:]:
            amount_user_day += 1
        if row[2][:-13:] == current_time[:-13:]:
            amount_user_hour += 1

        row = cursor.fetchone()

    msg = f"""
👥 <b>Пользователей</b>: <code>{amount_user_all}</code>
"""

    return msg

def count_screen(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET screen = screen + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_short(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET short = short + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_deanon(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET deanon = deanon + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_pass(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET gen_pass = gen_pass + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_name(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET gen_name = gen_name + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_proxies(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET proxies = proxies + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_tg(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET tg_id = tg_id + {value} WHERE user_id = "{user_id}"')
    conn.commit()

def count_ip(user_id, value):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET ip = ip + {value} WHERE user_id = "{user_id}"')
    conn.commit()


def click_url(url):
	urls = f'{config.clck_url}{url}'
	url = f"{config.clck_url_2}{url}"
	url2 = f"{config.clck_url_3}{url}"
	url3 = f"{config.clck_url_4}{url}"
	r1 = requests.get(urls)
	r2 = requests.get(url)
	r3 = requests.get(url2)
	r4 = requests.get(url3)
	url_s = r1.text
	url_1 = r2.text
	url_2 = r3.text
	url_3 = r4.text

	return url_1, url_2, url_3, url_s


def gen_proxy():
    proxy = requests.get('http://d4n13l3k00.ml/api/proxy/socks5?c=10').json()

    return proxy
