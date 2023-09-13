import re
import socks
import time
import config
import requests
import datetime
from telebot import types
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.messages import GetHistoryRequest, ReadHistoryRequest
from telethon import TelegramClient, events, sync
import telethon.sync
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import telebot
import json
import pymysql

import sqlite3
from urllib.request import urlopen

api_id = 988074
api_hash = 'a5ec8b7b6dbeedc2514ca7e4ba200c13'


client = TelegramClient('btc_pay', api_id, api_hash)
client.start()
bot_token = config.token

def connect():
	con = pymysql.connect(
		host='',
		user='',
		password='',
		database=''
	)
	cursor = con.cursor()
	return con, cursor

def main():
	connection,q = connect()
	global i
	q.execute(f"SELECT * FROM ugc_pays_btc where text != 'del'")
	info = q.fetchall()
	infoo = info
	for i in infoo:
		if i != None and i[2] != 'del':
			if i[3] == 'banker':
				client.send_message('BTC_CHANGE_BOT', f'/start {i[2]}')
				#bot = telebot.TeleBot(bot_token).send_message(825416463, f'/start {i[1].split("start=")[1]}')
				time.sleep(3)
				q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[2]}'")
				connection.commit()
				answer = check()
				if 'Вы получили' in str(answer) and 'RUB' in str(answer):
					summa_plus_balance = str(answer).split('(')[1].split(' ')[0]
					bot = telebot.TeleBot(bot_token).send_message(i[1], f'⚡️ Получили грязь через BTC Banker на {summa_plus_balance} RUB. В течение часа я отправлю тебе чистый чек.')
					send = types.InlineKeyboardMarkup()
					send.add(types.InlineKeyboardButton(text='Написать',callback_data=f'пишем:{i[1]}'))
					q.execute(f"update ugc_pays_btc set amount = '{summa_plus_balance}' where id = '{i[0]}'")
					connection.commit()
					if float(summa_plus_balance) <= 5000:
						bot = telebot.TeleBot(bot_token).send_message(config.chat_message, f'Пользователь: <a href="tg://user?id={i[1]}">{i[1]}</a>\n\nСистема: Banker\nСумма: {summa_plus_balance}\nДолжен получить: <code>{"%.2f" % (float(summa_plus_balance) - (float(summa_plus_balance)/100*5))}</code>',parse_mode='HTML',reply_markup=send)
					elif float(summa_plus_balance) > 5000:
						bot = telebot.TeleBot(bot_token).send_message(config.chat_message, f'Пользователь: <a href="tg://user?id={i[1]}">{i[1]}</a>\n\nСистема: Banker\nСумма: {summa_plus_balance}\nДолжен получить: <code>{"%.2f" % (float(summa_plus_balance) - (float(summa_plus_balance)/100*10))}</code>',parse_mode='HTML',reply_markup=send)

				elif 'Упс, кажется, данный чек успел обналичить кто-то другой 😟' in str(answer):
					bot = telebot.TeleBot(bot_token).send_message(i[1], '❗️ Ошибка в чеке')
					q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[2]}'")
					connection.commit()
				client.send_message('BTC_CHANGE_BOT', f'/start')

			else:
				client.send_message('Chatex_bot', f'/start {i[2].split("start=")[1]}')
				time.sleep(1)
				answer = check_chatex()
				q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[2]}'")
				connection.commit()
				if 'Ваучер на сумму' in str(answer) and 'BTC успешно активирован!' in str(answer):
					summa_plus_balance = str(answer).split('Ваучер на сумму ')[1].split(' BTC успешно активирован!')[0]
					data = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summa_plus_balance = "%.2f" % float(float(data) * float(summa_plus_balance))
					#bot = telebot.TeleBot(bot_token).send_message(config.chat_new_user, f'Пользователь: <a href="tg://user?id={i[0]}">{i[0]}</a>\nПополнил баланс на {summa_plus_balance} руб через BTC\nЧек: {i[1]}',parse_mode='HTML')
					bot = telebot.TeleBot(bot_token).send_message(i[1], f'⚡️ Получили грязь через Chatex на {summa_plus_balance} RUB. В течение часа я отправлю тебе чистый ваунчер.')
					send = types.InlineKeyboardMarkup()
					send.add(types.InlineKeyboardButton(text='Написать',callback_data=f'пишем:{i[1]}'))
					q.execute(f"update ugc_pays_btc set amount = '{summa_plus_balance}' where id = '{i[0]}'")
					connection.commit()
					if float(summa_plus_balance) <= 5000:
						bot = telebot.TeleBot(bot_token).send_message(config.chat_message, f'Пользователь: <a href="tg://user?id={i[1]}">{i[1]}</a>\n\nСистема: ChatEx\nСумма: {summa_plus_balance}\nДолжен получить: <code>{"%.2f" % (float(summa_plus_balance) - (float(summa_plus_balance)/100*5))}</code>',parse_mode='HTML',reply_markup=send)
					elif float(summa_plus_balance) > 5000:
						bot = telebot.TeleBot(bot_token).send_message(config.chat_message, f'Пользователь: <a href="tg://user?id={i[1]}">{i[1]}</a>\n\nСистема: ChatEx\nСумма: {summa_plus_balance}\nДолжен получить: <code>{"%.2f" % (float(summa_plus_balance) - (float(summa_plus_balance)/100*10))}</code>',parse_mode='HTML',reply_markup=send)
				elif 'Ваучер уже активирован' in str(answer):
					bot = telebot.TeleBot(bot_token).send_message(i[1], '❗️ Ошибка в ваучере')
					q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[2]}'")
					connection.commit()
				client.send_message('Chatex_bot', f'/start')


def check():
	channel_username='BTC_CHANGE_BOT'
	channel_entity=client.get_entity(channel_username)
	posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
	mesages = posts.messages
	for i in mesages:
		answer = i.message
		return answer


def check_chatex():
	channel_username='Chatex_bot'
	channel_entity=client.get_entity(channel_username)
	posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
	mesages = posts.messages
	for i in mesages:
		answer = i.message
		return answer

while True:
	time.sleep(2)
	main()

client.run_until_disconnected()