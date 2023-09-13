import re
import socks
import time
import config
import requests
import datetime
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.messages import GetHistoryRequest, ReadHistoryRequest
from telethon import TelegramClient, events, sync
import telethon.sync
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import telebot
import json
from tools.mysql import connect
import sqlite3
from urllib.request import urlopen

api_id = 
api_hash = ''


client = TelegramClient('sms', api_id, api_hash)
client.start()
bot_token = config.token



def main():
	connection,q = connect()
	global i
	q.execute(f"SELECT * FROM ugc_pays_btc where text != 'del'")
	info = q.fetchall()
	infoo = info
	for i in infoo:
		if i != None and i[1] != 'del':
			if i[5] == 'banker':
				time.sleep(1)
				client.send_message('BTC_CHANGE_BOT', f'/start {i[1]}')
				#bot = telebot.TeleBot(bot_token).send_message(825416463, f'/start {i[1].split("start=")[1]}')
				time.sleep(3)
				q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[1]}'")
				connection.commit()
				answer = check()
				if 'Вы получили' in str(answer) and 'RUB' in str(answer):
					summa_plus_balance = str(answer).split('(')[1].split(' ')[0]
					q.execute(f"update ugc_users set balance = balance + '{summa_plus_balance}' where userid = '{i[0]}'")
					connection.commit()
					now = datetime.datetime.now()
					nnow = str(now)[:19]
					q.execute(f"update ugc_pays_btc set date_pay = '{nnow}' where id = '{i[4]}'")
					connection.commit()
					q.execute(f"update ugc_pays_btc set summa = '{summa_plus_balance}' where id = '{i[4]}'")
					connection.commit()
					try:
						bot = telebot.TeleBot(bot_token).send_message(config.chat_new_user, f'Пользователь: <a href="tg://user?id={i[0]}">{i[0]}</a>\nПополнил баланс на {summa_plus_balance} руб через BTC\nЧек: {i[1]}',parse_mode='HTML')
					except:
						pass
					q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[1]}'")
					connection.commit()
					q.execute(f'SELECT ref1 FROM ugc_users WHERE userid = "{i[0]}"')
					ref1 = q.fetchone()
					if str(ref1[0]) != '0':
						addd = float(summa_plus_balance) /100 * 15
						q.execute(f"update ugc_users set balance = balance + '{addd}' where userid = '{ref1}'")
						connection.commit()
					try:
						bot = telebot.TeleBot(bot_token).send_message(i[0], f'⚡️ Вы пополнили свой баланс через BTC Banker на {summa_plus_balance} RUB. Приятных покупок.')
					except:
						pass
				elif 'Упс, кажется, данный чек успел обналичить кто-то другой 😟' in str(answer):
					try:
						bot = telebot.TeleBot(bot_token).send_message(i[0], 'Ошибка в чеке')
					except:
						pass
					q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[1]}'")
					connection.commit()
				client.send_message('BTC_CHANGE_BOT', f'/start')
				time.sleep(2)

			else:
				time.sleep(1)
				client.send_message('Chatex_bot', f'/start {i[1].split("start=")[1]}')
				bot = telebot.TeleBot(bot_token).send_message(825416463, f'/start {i[1].split("start=")[1]}')
				time.sleep(1)
				answer = check_chatex()
				q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[1]}'")
				connection.commit()
				if 'Ваучер на сумму' in str(answer) and 'BTC успешно активирован!' in str(answer):
					summa_plus_balance = str(answer).split('Ваучер на сумму ')[1].split(' BTC успешно активирован!')[0]
					data = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summa_plus_balance = "%.2f" % float(float(data) * float(summa_plus_balance))
					q.execute(f"update ugc_users set balance = balance + '{summa_plus_balance}' where userid = '{i[0]}'")
					connection.commit()
					now = datetime.datetime.now()
					nnow = str(now)[:19]
					q.execute(f"update ugc_pays_btc set date_pay = '{nnow}' where id = '{i[4]}'")
					connection.commit()
					q.execute(f"update ugc_pays_btc set summa = '{summa_plus_balance}' where id = '{i[4]}'")
					connection.commit()
					try:
						bot = telebot.TeleBot(bot_token).send_message(config.chat_new_user, f'Пользователь: <a href="tg://user?id={i[0]}">{i[0]}</a>\nПополнил баланс на {summa_plus_balance} руб через BTC\nЧек: {i[1]}',parse_mode='HTML')
					except:
						pass
					try:
						bot = telebot.TeleBot(bot_token).send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={i[0]}">{i[0]}</a>\nПополнил баланс на {summa_plus_balance} руб через BTC\nЧек: {i[1]}',parse_mode='HTML')
					except:
						pass
					q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[1]}'")
					connection.commit()
					q.execute(f'SELECT ref1 FROM ugc_users WHERE userid = "{i[0]}"')
					ref1 = q.fetchone()
					if str(ref1[0]) != '0':
						addd = float(summa_plus_balance) /100 * 15
						q.execute(f"update ugc_users set balance = balance + '{addd}' where userid = '{ref1}'")
						connection.commit()
					try:
						bot = telebot.TeleBot(bot_token).send_message(i[0], f'⚡️ Вы пополнили свой баланс через Chatex на {summa_plus_balance} RUB. Приятных покупок.')
					except:
						pass
				elif 'Ваучер уже активирован' in str(answer):
					try:
						bot = telebot.TeleBot(bot_token).send_message(i[0], 'Ошибка в чеке')
					except:
						pass
					q.execute(f"update ugc_pays_btc set text = 'del' where text = '{i[1]}'")
					connection.commit()
				client.send_message('Chatex_bot', f'/start')
				time.sleep(2)


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