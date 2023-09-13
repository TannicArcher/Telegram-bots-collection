import telebot
import time
import json
from telebot import types,apihelper
import datetime
import sqlite3
import requests
from config import connect

bot_token = '1549307401:AAFk--'
bot = telebot.AsyncTeleBot(bot_token)
admin_list = []


while True:
	time.sleep(20)
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_temp_sending')
	row = q.fetchall()
	now = datetime.datetime.now()
	today = str(now)
	for i in row:
		aa = 1
		if aa == 1:
			colvo_send_message_users = 0
			colvo_dont_send_message_users = 0
			# time.sleep(0.1)
			q.execute(f'SELECT userid FROM ugc_users')
			users = q.fetchall()
			aa = 0
			if i[2] != 'Нет':
				aa += 3
			if i[3] == '/':
				aa += 2
			# print(i[5])
			amm = 0

			bott = telebot.TeleBot(bot_token).send_message(admin_list[0],f'<b>Рассылка запущена</b>',parse_mode='HTML')
			for user in users:
				time.sleep(0.05)
				amm += 1
				print(user)
				if aa == 0:
					try:
						info = types.InlineKeyboardMarkup()
						info.add(types.InlineKeyboardButton(text='❌ Понятно',callback_data=f'реклама_удалить'))
						bot.send_message(user[0], str(i[1]), parse_mode='HTML')
						colvo_send_message_users = colvo_send_message_users + 1;
					except Exception as e:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
				elif aa == 1:
					try:
						info = types.InlineKeyboardMarkup()
						info.add(types.InlineKeyboardButton(text='❌ Понятно',callback_data=f'реклама_удалить'))
						bot.send_message(user[0], str(i[1]),parse_mode='HTML')
						colvo_send_message_users = colvo_send_message_users + 1;
					except Exception as e:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
				elif aa == 2:
					try:
						info = types.InlineKeyboardMarkup()
						info.add(types.InlineKeyboardButton(text='❌ Понятно',callback_data=f'реклама_удалить'))
						bot.send_message(user[0], str(i[1]),parse_mode='HTML')
						colvo_send_message_users = colvo_send_message_users + 1;
					except Exception as e:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
				else:
					try:
						info = types.InlineKeyboardMarkup()
						info.add(types.InlineKeyboardButton(text='❌ Понятно',callback_data=f'реклама_удалить'))
						bot.send_photo(user[0], photo=i[2], caption=str(i[1]),parse_mode='HTML')
						colvo_send_message_users = colvo_send_message_users + 1;
					except Exception as e:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1;

			q.execute(f'SELECT COUNT(userid) FROM ugc_users')
			users_count = q.fetchone()[0]
			for b in admin_list:
				bott = telebot.TeleBot(bot_token).send_message(b,f'<b>Рассылка завершена ✅\nКол-во пользователей: {users_count}</b>',parse_mode='HTML')
