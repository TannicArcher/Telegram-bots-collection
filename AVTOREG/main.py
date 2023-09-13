# -*- coding: utf-8 -*- 
import telebot
from telebot import types,apihelper
import time
from threading import Thread
import random
import traceback
import datetime
from smshuborg import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber, SetStatus, GetStatus,GetFreeSlotsAndPrices,ServiceStorage
import config
import requests
import keyboards
import json
from tools.SystemInfo import SystemInfo
import sqlite3
import texts
from decimal import Decimal
from tools.mysql import connect

last_time = {}
bot = telebot.TeleBot(config.token)
wrapper = Sms(config.token_sms)
admins_users = ['825416463','1151436944','717885554', '1735839466', '1151436944']


bot.send_message(1735839466,'Файл main.py перезапущен')


@bot.message_handler(commands=['start'])
def start_message(message):
  try:
  	print(message.chat.id)
  	if str(message.chat.type) == 'private':
  		if message.chat.id not in last_time:
  			last_time[message.chat.id] = time.time()
  			start_messages(message)
  		else:
  			if (time.time() - last_time[message.chat.id]) * 1000 < 800:
  				return 0
  			else:
  				start_messages(message)
  			last_time[message.chat.id] = time.time()
  except:
    pass

def start_messages(message):
	userid = str(message.chat.id)
	username = str(message.from_user.username)
	print(message.chat.id)
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
	row = q.fetchone()
	q.execute(f'SELECT first_photo_fileid FROM ugc_settings')
	file_id = q.fetchone()[0]
	if row is None:
		if len(message.text) > 6:
			ref_infa = q.execute(f'SELECT * FROM ugc_users where userid = "{message.text[7:]}"').fetchall()
			now = datetime.datetime.now()
			today = str(now)
			bot.send_message(config.chat_new_user, f'Новый пользователь: <a href="tg://user?id={userid}">{userid}</a>\nРефовод: <a href="tg://user?id={message.text[7:]}">{message.text[7:]}</a>',parse_mode='HTML')
			q.execute("INSERT INTO ugc_users (userid,ref1,date_reg) VALUES  ('%s', '%s', '%s')"%(userid,i[1],today[:16]))
			connection.commit()
		else:
			now = datetime.datetime.now()
			today = str(now)
			bot.send_message(config.chat_new_user, f'Новый пользователь: <a href="tg://user?id={userid}">{userid}</a>',parse_mode='HTML')
			q.execute("INSERT INTO ugc_users (userid,date_reg) VALUES ('%s','%s')"%(userid,today[:16]))
			connection.commit()
	q.execute(f'SELECT id FROM ugc_bans WHERE userid = "{userid}"')
	row = q.fetchone()
	if row == None:
		photo = open('dmenu.jpg', 'rb')
		bot.send_photo(message.chat.id, photo,parse_mode='HTML',reply_markup=keyboards.main())


@bot.message_handler(content_types=['photo'])
def send_text(message):
	print(message)

def check_ban(userid):
	connection,q = connect()
	q.execute(f'SELECT id FROM ugc_bans WHERE userid = "{userid}"')
	row = q.fetchone()
	if row == None:
		return 'unban'
	else:
		return 'ban'


@bot.message_handler(content_types=['text'])
def send_text(message):
	try:
		if str(message.chat.type) != 'private':
			if message.text[:5] == '/give':
				connection,q = connect()
			
				am = message.text.split(' ')
				q.execute(f'SELECT balance FROM ugc_users WHERE userid = "{message.from_user.id}"')
				entit = q.fetchone()
				if float(entit[0]) >= float(am[2]):
					q.execute(f"""update ugc_users set balance = balance - '{am[2]}' where userid = '{message.from_user.id}'""")
					connection.commit()
					q.execute(f"""update ugc_users set balance = balance + '{am[2]}' where userid = '{am[1]}'""")
					connection.commit()
					bot.send_message(message.chat.id,'Перевод совершен')
				else:
					bot.send_message(message.chat.id,'Баланса не хватает')
			if message.text == '/balance':
				connection,q = connect()
			
				am = message.text.split(' ')
				q.execute(f'SELECT balance FROM ugc_users WHERE userid = "{message.from_user.id}"')
				entit = q.fetchone()
				bot.send_message(message.chat.id,f'<a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>, твой баланс: {"%.2f" %float(entit[0])} ₽',parse_mode='html')
			if message.text == '/id':
				bot.send_message(message.chat.id,f'{message.from_user.id}')

		if str(message.chat.type) == 'private':
			connection,q = connect()
		
			q.execute(f'SELECT id FROM ugc_bans WHERE userid = "{message.chat.id}"')
			row = q.fetchone()
			if row == None:
				if message.chat.id not in last_time:
					last_time[message.chat.id] = time.time()
					if '/getuser ' in message.text and str(message.chat.id) in admins_users:
						user = message.text.split(' ')[1]
						UsrInfo = bot.get_chat_member(user, user).user

						bot.send_message(message.chat.id, f'<a href="tg://user?id={user}">{user}</a>\nId: ' + str(UsrInfo.id) + "\nFirst Name: " + str(UsrInfo.first_name) + "\nLast Name: " + str(UsrInfo.last_name) + "\nUsername: @" + str(UsrInfo.username), parse_mode='html')
					

					if message.text == '/admin' and str(message.chat.id) in admins_users:
						markup = types.InlineKeyboardMarkup(row_width=1)
						markup.add(
						types.InlineKeyboardButton(text='ℹ️ Информаци о сервере', callback_data='admin_info_server'),
						types.InlineKeyboardButton(text='ℹ️ Информация', callback_data='admin_info'),
						types.InlineKeyboardButton(text='ℹ️ BAN LIST', callback_data='admin_ban_list'),
						types.InlineKeyboardButton(text='🔧 Изменить баланс', callback_data='give_balance'),
						types.InlineKeyboardButton(text='⚙️ Рассылка', callback_data='email_sending'),
						types.InlineKeyboardButton(text='⚙️ Кнопки', callback_data='admin_buttons'),
						types.InlineKeyboardButton(text='⚙️ Номера', callback_data='admin_numbers'),
						)
						msg = bot.send_message(message.chat.id, '<b>❤️ Держи менюшку, красавчик ❤️</b>',parse_mode='HTML',reply_markup=markup)
					if '/ban ' in message.text and str(message.chat.id) in admins_users:
						connection,q = connect()
					
						q.execute("INSERT INTO ugc_bans (userid) VALUES  ('%s')"%(message.text[5:]))
						connection.commit()
						bot.send_message(message.chat.id, f'<b>Пользователь <a href="tg://user?id={message.text[5:]}">{message.text[5:]}</a> забанен</b>',parse_mode='HTML')

					if '/unban ' in message.text and str(message.chat.id) in admins_users:
						connection,q = connect()
					
						q.execute(f'DELETE FROM ugc_bans WHERE userid = "{message.text[7:]}"')
						connection.commit()
						bot.send_message(message.chat.id, f'<b>Пользователь <a href="tg://user?id={message.text[7:]}">{message.text[7:]}</a> разбанен</b>',parse_mode='HTML')


					if message.text == '👤 Профиль':
						msg = bot.send_message(message.chat.id, texts.profile(message),parse_mode='HTML',reply_markup=keyboards.profile)

					elif message.text == '🌺 Мультисервис':
						bot.send_message(message.chat.id, '🌺 <b>Мультисервис</b> - Покупка нескольких сервисов на один номер.\n\nСтоимость каждого сервиса будет увеличена на <b>20%</b> от цены что действует при их покупке <b>отдельно</b>',parse_mode='HTML', reply_markup=keyboards.mult_menu)

					elif message.text == 'ℹ️ INFO':
						bot.send_message(message.chat.id, texts.text_faq,parse_mode='html')

					elif message.text == '/info':
						bot.send_message(message.chat.id,texts.info,parse_mode='HTML')

					elif message.text == '🔥 Номера':
						bot.send_message(message.chat.id, texts.main(message.chat.id),parse_mode='HTML', reply_markup=keyboards.services_list())

					elif message.text == '💣 Аренда':
						bot.send_message(message.chat.id, '♻️ Меню аренды номеров',parse_mode='HTML', reply_markup=keyboards.rent_menu)

					elif message.text == 'f':
						bot.send_message(message.chat.id, '<b>ам</b>',parse_mode='HTML')

					elif 'BTC_CHANGE_BOT?start='.lower() in message.text.lower():
						for i in message.entities:
							if i.type == 'url' or i.type == 'text_link':
								connection,q = connect()
							
							#bot.send_message('-1001270414760', message.text.split('start=')[1])
								delete = types.InlineKeyboardMarkup()
								delete.add(types.InlineKeyboardButton(text=f'🔚 Скрыть сообщение', callback_data='скрыть'))
								bot.send_message(message.chat.id,'🏵 Чек получен! Идет проверка...',reply_markup=delete)
								q.execute("INSERT INTO ugc_pays_btc (userid,text,bot) VALUES ('%s','%s','%s')"%(message.chat.id, message.text.split('start=')[1], 'banker'))
								connection.commit()
						
					elif 'Chatex_bot?start='.lower() in message.text.lower():
						for i in message.entities:
							if i.type == 'url' or i.type == 'text_link':
								connection,q = connect()
							
							# bot.send_message('-1001270414760', message.text.split('start=')[1])
								delete = types.InlineKeyboardMarkup()
								delete.add(types.InlineKeyboardButton(text=f'🔚 Скрыть сообщение', callback_data='скрыть'))
								bot.send_message(message.chat.id,'🏵 Чек получен! Идет проверка...',reply_markup=delete)
								q.execute("INSERT INTO ugc_pays_btc (userid,text,bot) VALUES ('%s','%s','%s')"%(message.chat.id, message.text, 'chatex'))
								connection.commit()

					
					else:
						connection,q = connect()
						
						q.execute(f'SELECT * FROM ugc_ads_button WHERE name = "{message.text}"')
						row = q.fetchone()
						q.execute(f'SELECT entit FROM ugc_ads_button WHERE name = "{message.text}"')
						entit = q.fetchone()
						if row != None:
							json_text = eval(entit[0])
							aa = 0
							if row[3] != 'Нет':
								aa += 1
							if row[4] != 'Нет':
								aa += 2

							if aa == 0:
							# bot.send_message(message.chat.id,row[2],parse_mode='HTML')
								response = requests.post(
								url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendMessage"),
								data={'chat_id': str(message.chat.id), 'text': str(row[2]),'entities': json.dumps(json_text)}).json()

							elif aa == 1:
								response = requests.post(
								url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendPhoto"),
								data={'chat_id': str(message.chat.id), 'photo': str(row[3]), 'caption': str(row[2]),'caption_entities': json.dumps(json_text)}).json()

							# bot.send_photo(message.chat.id,row[3],row[2],parse_mode='HTML')
							elif aa == 2:
							# keyboard = types.InlineKeyboardMarkup(row_width=1)
							# keyboard.add(types.InlineKeyboardButton(text='Перейти',url=f'{row[4]}'))
								reply = json.dumps({'inline_keyboard': [[{'text': '🔥 Перейти ', 'url': f'{row[4]}'}]]})
								response = requests.post(
									url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendMessage"),
									data={'chat_id': str(message.chat.id), 'text': str(row[2]), 'reply_markup': str(reply),'entities': json.dumps(json_text)}).json()

							# bot.send_message(message.chat.id,row[2],parse_mode='HTML',reply_markup=keyboard)
							else:
								reply = json.dumps({'inline_keyboard': [[{'text': '🔥 Перейти ', 'url': f'{row[4]}'}]]})
								response = requests.post(
									url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendPhoto"),
									data={'chat_id': str(message.chat.id), 'photo': str(row[3]), 'caption': str(row[2]), 'reply_markup': str(reply),'caption_entities': json.dumps(json_text)}).json()
				else:
					if (time.time() - last_time[message.chat.id]) * 1000 < 800:
						return 0
					else:
						if message.text == '/admin' and str(message.chat.id) in admins_users:
							markup = types.InlineKeyboardMarkup(row_width=1)
							markup.add(
							types.InlineKeyboardButton(text='ℹ️ Информаци о сервере', callback_data='admin_info_server'),
							types.InlineKeyboardButton(text='ℹ️ Информация', callback_data='admin_info'),
							types.InlineKeyboardButton(text='ℹ️ BAN LIST', callback_data='admin_ban_list'),
							types.InlineKeyboardButton(text='🔧 Изменить баланс', callback_data='give_balance'),
							types.InlineKeyboardButton(text='⚙️ Рассылка', callback_data='email_sending'),
							types.InlineKeyboardButton(text='⚙️ Кнопки', callback_data='admin_buttons'),
							types.InlineKeyboardButton(text='⚙️ Номера', callback_data='admin_numbers'),
							)
							msg = bot.send_message(message.chat.id, '<b>❤️ Держи менюшку, красавчик ❤️</b>',parse_mode='HTML',reply_markup=markup)

						if '/ban ' in message.text and str(message.chat.id) in admins_users:
							connection,q = connect()
						
							q.execute("INSERT INTO ugc_bans (userid) VALUES  ('%s')"%(message.text[5:]))
							connection.commit()
							bot.send_message(message.chat.id, f'<b>Пользователь <a href="tg://user?id={message.text[5:]}">{message.text[5:]}</a> забанен</b>',parse_mode='HTML')

						if '/unban ' in message.text and str(message.chat.id) in admins_users:
							connection,q = connect()
						
							q.execute(f'DELETE FROM ugc_bans WHERE userid = "{message.text[7:]}"')
							connection.commit()
							bot.send_message(message.chat.id, f'<b>Пользователь <a href="tg://user?id={message.text[7:]}">{message.text[7:]}</a> разбанен</b>',parse_mode='HTML')

						if '/set_price' in message.text and str(message.chat.id) in admins_users:
							connection,q = connect()
						
							answer = message.text.split(' ')
							q.execute(f'SELECT * FROM ugc_country WHERE idd = "{answer[2]}"')
							country = q.fetchone()[0]
							q.execute(f"""update ugc_service_all set price = '{answer[3]}' where code = '{answer[1]}' and country = '{country}'""")
							connection.commit()
							bot.send_message(message.chat.id, 'Успешно',parse_mode='html')


						if message.text == '👤 Профиль':
							msg = bot.send_message(message.chat.id, texts.profile(message),parse_mode='HTML',reply_markup=keyboards.profile)

						elif message.text == 'ℹ️ INFO':
							bot.send_message(message.chat.id, texts.text_faq,parse_mode='html')

						elif message.text == '/info':
							bot.send_message(message.chat.id,texts.info,parse_mode='HTML')

						elif message.text == '🔥 Номера':
							bot.send_message(message.chat.id, texts.main(message.chat.id),parse_mode='HTML', reply_markup=keyboards.services_list())

						elif message.text == '💣 Аренда':
							bot.send_message(message.chat.id, '♻️ Меню аренды номеров',parse_mode='HTML', reply_markup=keyboards.rent_menu)

						elif message.text == '🌺 Мультисервис':
							bot.send_message(message.chat.id, '🌺 <b>Мультисервис</b> - Покупка нескольких сервисов на один номер.\n\nСтоимость каждого сервиса будет увеличена на <b>20%</b> от цены что действует при их покупке <b>отдельно</b>',parse_mode='HTML', reply_markup=keyboards.mult_menu)

						elif message.text == 'f':
							bot.send_message(message.chat.id, '<b>ам</b>',parse_mode='HTML')

						elif 'BTC_CHANGE_BOT?start='.lower() in message.text.lower():
							for i in message.entities:
								if i.type == 'url' or i.type == 'text_link':
									connection,q = connect()
								
								#bot.send_message('-1001270414760', message.text.split('start=')[1])
									delete = types.InlineKeyboardMarkup()
									delete.add(types.InlineKeyboardButton(text=f'🔚 Скрыть сообщение', callback_data='скрыть'))
									bot.send_message(message.chat.id,'🏵 Чек получен! Идет проверка...',reply_markup=delete)
									q.execute("INSERT INTO ugc_pays_btc (userid,text,bot) VALUES ('%s','%s','%s')"%(message.chat.id, message.text.split('start=')[1], 'banker'))
									connection.commit()
						
						elif 'Chatex_bot?start='.lower() in message.text.lower():
							for i in message.entities:
								if i.type == 'url' or i.type == 'text_link':
									connection,q = connect()
								
									# bot.send_message('-1001270414760', message.text.split('start=')[1])
									delete = types.InlineKeyboardMarkup()
									delete.add(types.InlineKeyboardButton(text=f'🔚 Скрыть сообщение', callback_data='скрыть'))
									bot.send_message(message.chat.id,'🏵 Чек получен! Идет проверка...',reply_markup=delete)
									q.execute("INSERT INTO ugc_pays_btc (userid,text,bot) VALUES ('%s','%s','%s')"%(message.chat.id, message.text, 'chatex'))
									connection.commit()

						else:
							connection,q = connect()
						
							q.execute(f'SELECT * FROM ugc_ads_button WHERE name = "{message.text}"')
							row = q.fetchone()
							q.execute(f'SELECT entit FROM ugc_ads_button WHERE name = "{message.text}"')
							entit = q.fetchone()
							if row != None:
								json_text = eval(entit[0])
								aa = 0
								if row[3] != 'Нет':
									aa += 1
								if row[4] != 'Нет':
									aa += 2

								if aa == 0:
									# bot.send_message(message.chat.id,row[2],parse_mode='HTML')
									response = requests.post(
										url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendMessage"),
										data={'chat_id': str(message.chat.id), 'text': str(row[2]),'entities': json.dumps(json_text)}).json()

								elif aa == 1:
									response = requests.post(
										url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendPhoto"),
										data={'chat_id': str(message.chat.id), 'photo': str(row[3]), 'caption': str(row[2]),'caption_entities': json.dumps(json_text)}).json()

								# bot.send_photo(message.chat.id,row[3],row[2],parse_mode='HTML')
								elif aa == 2:
								# keyboard = types.InlineKeyboardMarkup(row_width=1)
								# keyboard.add(types.InlineKeyboardButton(text='Перейти',url=f'{row[4]}'))
									reply = json.dumps({'inline_keyboard': [[{'text': '🔥 Перейти ', 'url': f'{row[4]}'}]]})
									response = requests.post(
										url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendMessage"),
										data={'chat_id': str(message.chat.id), 'text': str(row[2]), 'reply_markup': str(reply),'entities': json.dumps(json_text)}).json()

								# bot.send_message(message.chat.id,row[2],parse_mode='HTML',reply_markup=keyboard)
								else:
									reply = json.dumps({'inline_keyboard': [[{'text': '🔥 Перейти ', 'url': f'{row[4]}'}]]})
									response = requests.post(
										url='https://api.telegram.org/bot{0}/{1}'.format(config.token, "sendPhoto"),
										data={'chat_id': str(message.chat.id), 'photo': str(row[3]), 'caption': str(row[2]), 'reply_markup': str(reply),'caption_entities': json.dumps(json_text)}).json()

					last_time[message.chat.id] = time.time()
	except:pass

def edit_balans(message):
	# try:
		connection,q = connect()
		
		am = message.text.split("\n")
		q.execute(f"update ugc_users set balance = '{am[1]}' where userid = '{am[0]}'")
		connection.commit()
		bot.send_message(message.chat.id, '<b>Успешно</b>',parse_mode='HTML')
	# except:
	# 	bot.send_message(message.chat.id, '<b>Ошибка в параметрах</b>',parse_mode='HTML')

def button_admin(message):
	if message.text[:5] != '/del ':
		connection,q = connect()
		
		url = message.text.split('\n')[0]
		image = message.text.split('\n')[1]
		name = message.text.split('\n')[2]
		q.execute("INSERT INTO ugc_ads_button (name,image,button) VALUES ('%s','%s','%s')"%(name,image,url))
		connection.commit()
		mmsg = bot.send_message(message.chat.id,f'<b>Введите текст кнопки</b>',parse_mode='HTML')
		bot.register_next_step_handler(mmsg, text_button_admin,name)
	else:
		connection,q = connect()
		
		q.execute(f"DELETE FROM ugc_ads_button WHERE name='{message.text[5:]}'")
		connection.commit()
		bot.send_message(message.chat.id,f'<b>Успешно</b>',parse_mode='HTML')

def text_button_admin(message,rent_name):
	json_entit = None
	if 'entities' in message.json:
		json_entit = str(message.json['entities'])

	print(str(json_entit))
	text_send = message.text

	connection,q = connect()
	q.execute(f"update ugc_ads_button set text = '{text_send}' where name = '{rent_name}'")
	connection.commit()
	q.execute('update ugc_ads_button set entit = "{}" where name = "{}"'.format(json_entit, rent_name))
	connection.commit()
	msg = bot.send_message(message.chat.id,f'<b>Кнопка добавлена</b>',parse_mode='HTML')


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	msg = call.data
	try:
		connection,q = connect()
		
		q.execute(f'SELECT id FROM ugc_bans WHERE userid = "{call.message.chat.id}"')
		row = q.fetchone()
		if row == None:
			if str(msg) == 'email_sending':
				if str(call.message.chat.id) in admins_users:
					mmsg = bot.send_message(call.message.chat.id, 'Введите текст рассылки',parse_mode='HTML')
					bot.register_next_step_handler(mmsg, send_photoorno)
			if str(msg) == 'admin_numbers':
				if str(call.message.chat.id) in admins_users:
					doc = open('tools/service_list.txt', 'rb')
					bot.send_document(call.message.chat.id, doc, caption='''Для установки цены воспользуйтесь командой:
	<b>/set_price код_сервиса код_страны цена</b>

	Пример:<b> /set_price av 0 5</b>
	Коды стран:<i>
	0 - Россия
	1 - Украина
	2 - Казахстан
	51 - Беларусь
	32 - Румыния
	15 - Польша
	34 - Эстония
	40 - Узбекистан
	83 - Болгария
	78 - Франция
	12 - США
	85 - Молдова
	</i>

	Коды сервисов в файле''',parse_mode='html')
		
			if str(msg) == 'admin_info_server':
				if str(call.message.chat.id) in admins_users:
					bot.send_message(chat_id=call.message.chat.id, text=SystemInfo.get_info_text(), parse_mode='html')

			if str(msg) == 'admin_info':
				if str(call.message.chat.id) in admins_users:
					bot.send_message(chat_id=call.message.chat.id, text=texts.admin_stata(), parse_mode='html')

			if str(msg) == 'admin_ban_list':
				if str(call.message.chat.id) in admins_users:
					connection,q = connect()
					
					q.execute(f'SELECT * FROM ugc_bans')
					row = q.fetchall()
					text = ''
					for i in row:
						text = f'{text}<a href="tg://user?id={i[1]}">{i[1]}</a>, '
					bot.send_message(call.message.chat.id,f'''Для бана используйте команду /ban user_id
	Для разбана используйте команду /unban user_id
	Забаненные перцы:\n{text}''',parse_mode='html')

			if str(msg) == 'give_balance':
				if str(call.message.chat.id) in admins_users:
					mmsg = bot.send_message(call.message.chat.id, f'Введите данные в таком формате:\nид пользователя\nкакой баланс поставить пользователю')
					bot.register_next_step_handler(mmsg, edit_balans)



			if str(msg) == 'admin_buttons':
				if str(call.message.chat.id) in admins_users:
					mmsg = bot.send_message(call.message.chat.id, '<b>Если нужно удалить кнопку, то введи /del название кнопки\n\nДля добавления: введите нужны аргументы в таком виде:\n\nСсылка куда отправит кнопка\nСсылка на картинку\nНазвание\n\nЕсли что-то из этого не нужно, то напишите "Нет", если отправить нужно сейчас, то введите там "Нет"</b>',parse_mode='HTML')
					bot.register_next_step_handler(mmsg, button_admin)


				# if str(msg) == 'admin_info_server':
				# 	bot.send_message(chat_id=call.message.chat.id, text=SystemInfo.get_info_text(), parse_mode='html')

			if 'вернуться_' in str(str(msg)):
				if str(msg) == 'вернуться_назад':
					bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				if str(msg) == 'вернуться_аренда':
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'♻️ Меню аренды номеров',parse_mode='HTML', reply_markup=keyboards.rent_menu)
				if str(msg) == 'вернуться_сервисы_аренда':
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'♻️ Выберите нужный вам сервис', parse_mode='html',reply_markup=keyboards.rent_list())
				if 'вернуться_сервисы_аренда_' in str(msg):
					btn = types.InlineKeyboardMarkup()
					btn.add(types.InlineKeyboardButton(text='🇷🇺 Россия',callback_data=f'аренда_россия_{str(msg)[25:]}'))
					btn.add(types.InlineKeyboardButton(text='🔙',callback_data=f'вернуться_сервисы_аренда'))
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'🏳️‍🌈 Выберите нужную вам страну', parse_mode='html',reply_markup=btn)
				# if 'вернуться_время_аренда_' in str(msg):
				# 	am = keyboards.rent_spisok_time(str(msg)[23:])
				# 	if str(am) != 'Не удалось найти номер':
				# 		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				# 		bot.send_message(call.message.chat.id, '🕐 Выберите срок на который хотите арендовать номер', reply_markup = keyboards.rent_spisok_time(str(msg)[23:]))
				# 	else:
				# 		bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="В данный момент номера для этого сервиса не доступны")





			if str(msg) == 'мои_рефералы':
				bot.send_message(call.message.chat.id, texts.referals(call.message.chat.id),parse_mode='HTML')

			if str(msg) == 'пополнить_баланс':
				deposit_keyb = types.InlineKeyboardMarkup()
				deposit_keyb.add(types.InlineKeyboardButton(text='QIWI',callback_data=f'пополнить_баланс_qiwi'))
				deposit_keyb.add(types.InlineKeyboardButton(text='BANKER',callback_data=f'пополнить_баланс_btc'),types.InlineKeyboardButton(text='CHATEX',callback_data=f'пополнить_баланс_chatex'))
				bot.send_message(call.message.chat.id, f'''<b>Выберите способ пополнения баланса.</b>''',parse_mode='HTML',reply_markup=deposit_keyb)


			if str(msg) == 'пополнить_баланс_qiwi':
				connection,q = connect()
				
				q.execute(f'SELECT * FROM ugc_settings')
				row = q.fetchone()
				deposit_keyb = types.InlineKeyboardMarkup()
				deposit_keyb.add(types.InlineKeyboardButton(text='Оплатить ➲',url=f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={config.qiwi_number}&amountFraction=0&extra%5B%27comment%27%5D={call.message.chat.id}&currency=643&blocked[0]=account'))
				deposit_keyb.add(types.InlineKeyboardButton(text='В главное меню',callback_data=f'вернуться_назад'))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = texts.qiwi_pay(call.message.chat.id),parse_mode='HTML',reply_markup=deposit_keyb)

			if str(msg) == 'пополнить_баланс_btc':
				deposit_keyb = types.InlineKeyboardMarkup()
				deposit_keyb.add(types.InlineKeyboardButton(text='В главное меню',callback_data=f'вернуться_назад'))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Для оплаты чеком, просто отправьте его в чат 👇👇👇',parse_mode='HTML',reply_markup=deposit_keyb)

			if str(msg) == 'пополнить_баланс_chatex':
				deposit_keyb = types.InlineKeyboardMarkup()
				deposit_keyb.add(types.InlineKeyboardButton(text='В главное меню',callback_data=f'вернуться_назад'))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Для оплаты ваунчером, просто отправьте его в чат 👇👇👇',parse_mode='HTML',reply_markup=deposit_keyb)


			if 'история_аренда' in str(msg):
				if str(msg) == 'история_аренда':
					connection,q = connect()
					q.execute(f'SELECT * FROM ugc_rent_list where userid = "{call.message.chat.id}" and activ = "1"')
					row = q.fetchone()
					if row == None:
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'''<b>📜 Тут вы можите найти список арендованных номеров, а также просмотреть историю смс уведомлений</b>''',parse_mode='HTML',reply_markup=keyboards.rent_activ(call.message.chat.id))
					else:
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'''<b>📜 Тут вы можите найти список арендованных номеров, а также просмотреть историю смс уведомлений</b>''',parse_mode='HTML',reply_markup=keyboards.rent_activ(call.message.chat.id))
				else:
					am = texts.rent_text_activ(call.message.chat.id,str(msg)[14:])
					if str(am) != 'Номер завершил работу':
						deposit_keyb = types.InlineKeyboardMarkup()
						deposit_keyb.add(types.InlineKeyboardButton(text='✖️ Отменить',callback_data=f'отменить_аренда_{str(msg)[14:]}'))
						bot.send_message(call.message.chat.id, texts.rent_text_activ(call.message.chat.id,str(msg)[14:]),parse_mode='HTML',reply_markup=deposit_keyb)
					elif 'НОМЕР ЗАВЕРШИЛ РАБОТУ' in str(am):
						bot.send_message(call.message.chat.id, texts.rent_text_activ(call.message.chat.id,str(msg)[14:]),parse_mode='HTML')
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'''<b>📜 Тут вы можите найти список арендованных номеров, а также просмотреть историю смс уведомлений</b>''',parse_mode='HTML',reply_markup=keyboards.rent_activ(call.message.chat.id))
					else:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=am)

						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'''<b>📜 Тут вы можите найти список арендованных номеров, а также просмотреть историю смс уведомлений</b>''',parse_mode='HTML',reply_markup=keyboards.rent_activ(call.message.chat.id))

			if 'купитьмулт' in str(msg):
				connection,q = connect()
				tovars_text = msg.split(':')
				del tovars_text[0]
				pricee = 0
				tovars = ''
				for i in tovars_text:
					q.execute(f'SELECT * FROM ugc_mult_service where tag = "{i}"')
					price_phone = q.fetchone()
					tovars = f'{tovars}{price_phone[1]} '
					pricee += price_phone[3]
				btn = types.InlineKeyboardMarkup()
				btn.add(types.InlineKeyboardButton(text='💸 Заказать',callback_data=f'покупаеммулт{msg.replace("купитьмулт", "")}:{pricee}'))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'''<b>🌺 Мультисервис\n\n🧑‍💻 Выбраные сервисы: {tovars}\n💰 Стоимость номера: <code>{pricee} ₽</code></b>''',parse_mode='HTML',reply_markup=btn)

			if 'покупаеммулт' in msg:
				if call.message.chat.id not in last_time:
					last_time[call.message.chat.id] = time.time()
				else:
					if (time.time() - last_time[call.message.chat.id]) * 1000 < 2000:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Между запросами должно пройти 5 сек.")
						return 0
					else:
						last_time[call.message.chat.id] = time.time()
						connection,q = connect()
						tovars_text = msg.split(':')
						del tovars_text[0]
						q.execute(f'SELECT * FROM ugc_users where userid = "{call.message.chat.id}"')
						users_infa = q.fetchone()
						amm = ''
						if float(users_infa[2]) >= float(tovars_text[-1]):
							del tovars_text[-1]
							if len(tovars_text) == 1:
								amm = f'{tovars_text[0]}'
							if len(tovars_text) == 2:
								amm = f'{tovars_text[0]},{tovars_text[1]}'
							if len(tovars_text) == 3:
								amm = f'{tovars_text[0]},{tovars_text[1]},{tovars_text[2]}'
							response = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getMultiServiceNumber&multiService={amm}&country=0')
							if str(response.text) == 'NO_BALANCE':
								for user in config.admin:
									bot.send_message(user, 'Пополните баланс на smsactivate')
							elif str(response.text) == 'NO_NUMBERS':
								bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🌧 Не смогли найти номер")
							elif str(response.text) == 'BAD_SERVICE':
								bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🌧 Не смогли найти номер")
							else:
								print(response.text)
								tovasrs_text = msg.split(':')
								q.execute(f"update ugc_users set balance = balance - '{tovasrs_text[-1]}' where userid = '{call.message.chat.id}'")
								connection.commit()
								now = datetime.datetime.now()
								for i in response.json():
									q.execute(f'''SELECT * FROM ugc_mult_service where tag = "{i['service']}"''')
									service_infa = q.fetchone()
									btn = types.InlineKeyboardMarkup()
									btn.add(types.InlineKeyboardButton(text='👋 Отменить',callback_data=f'отменить_смс_{i["activation"]}_{service_infa[3]}'))
									q.execute("INSERT INTO ugc_phones (userid,nubmer,service,price,phone_id,site,sms,date_get) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(call.message.chat.id,i['phone'],service_infa[1],service_infa[3],i['activation'],'smsactivate','2',now.strftime("%Y-%m-%d %H:%M:%S")))
									connection.commit()
									bot.send_message(call.message.chat.id, f'''<b>❤️ Сервис: <code>{service_infa[1]}</code>
📱 Ваш номер: <code>{response.json()[0]["phone"]}</code>

Если смс не прийдет через 5 минут, то вам вернуться потраченные деньги за этот номер, аренда номера будет отменена!!!</b>''',parse_mode='HTML', reply_markup=btn)
								bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил мультисервис номер ({response.json()[0]["phone"]}), сервисы: {tovars_text}',parse_mode='HTML')
						else:
							bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💔 Баланса не хватает")



			if msg == 'вернуться_му':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text ='🌺 <b>Мультисервис</b> - Покупка нескольких сервисов на один номер.\n\nСтоимость каждого сервиса будет увеличена на <b>20%</b> от цены что действует при их покупке <b>отдельно</b>',parse_mode='HTML', reply_markup=keyboards.mult_menu)

			if 'мульт' in str(msg):
				connection,q = connect()
				tovars_text = msg.split(':')
				del tovars_text[0]
				price = float(0)
				if len(tovars_text) > 0:
					for i in tovars_text:
						aa = 0
						if len(tovars_text) > 3:
							if str(i) != tovars_text[0]:
								aa += 1
							if str(i) != tovars_text[1]:
								aa += 1
							if str(i) != tovars_text[2]:
								aa += 1

							if str(aa) == '3':
								q.execute(f'SELECT * FROM ugc_mult_service where tag = "{i}"')
								price_first = q.fetchone()
								msg = msg.replace(f":{price_first[2]}", '')
								del tovars_text[3]
								bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Максимум 3 сервиса')
							else:
								if tovars_text.count(i) > 1:
									q.execute(f'SELECT * FROM ugc_mult_service where tag = "{i}"')
									price_first = q.fetchone()
									msg = msg.replace(f":{price_first[2]}", '')
									tovars_text.remove(i)
						else:
							if tovars_text.count(i) != 1:
								q.execute(f'SELECT * FROM ugc_mult_service where tag = "{i}"')
								price_first = q.fetchone()
								msg = msg.replace(f":{price_first[2]}", '')
								# tovars_text.remove(i)
								tovars_text.remove(i)
				else:
					msg = msg.replace(f":", '')
				
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'🌺 Выберите нужные вам сервисы (не более 3)', parse_mode='html',reply_markup=keyboards.mult_list(msg))





			if str(msg) == 'аренда':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'♻️ Выберите нужный вам сервис', parse_mode='html',reply_markup=keyboards.rent_list())

			if 'аренда_купить' in str(msg):
				# bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				btn = types.InlineKeyboardMarkup()
				btn.add(types.InlineKeyboardButton(text='🇷🇺 Россия',callback_data=f'аренда_россия_{str(msg)[13:]}'))
				btn.add(types.InlineKeyboardButton(text='🔙',callback_data=f'вернуться_сервисы_аренда'))
				# bot.send_message(call.message.chat.id, '🏳️‍🌈 Выберите нужную вам страну',reply_markup=keyboar)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'🏳️‍🌈 Выберите нужную вам страну', parse_mode='html',reply_markup=btn)

			if 'аренда_россия_' in str(msg):
				am = keyboards.rent_spisok_time(str(msg)[14:])
				if str(am) != 'Не удалось найти номер':
					bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
					bot.send_message(call.message.chat.id, '🕐 Выберите срок на который хотите арендовать номер', reply_markup = keyboards.rent_spisok_time(str(msg)[14:]))
				else:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="В данный момент номера для этого сервиса не доступны")


			if 'аренда_время' in str(msg):
				connection,q = connect()
				
				response = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentServicesAndCountries&rent_time={str(msg).split("_")[2]}&country=0').json()
				am = response['services'][str(msg).split("_")[3]]['quant']
				if response['services'][str(msg).split("_")[3]]['quant'] != 0:
					q.execute(f'SELECT * FROM ugc_service_all WHERE code = "{str(msg).split("_")[3]}" and rent = "1"')
					rent = q.fetchone()
					price = str(msg).split('_')[4]
					rent_buy = types.InlineKeyboardMarkup()
					rent_buy.add(types.InlineKeyboardButton(text=f'💳 Арендовать за {"%.2f" % (float(price))} RUB',callback_data=f'купить_аренда_{str(msg).split("_")[3]}_{str(msg).split("_")[2]}_{"%.2f" % (float(price))}'))
					# rent_buy.add(types.InlineKeyboardButton(text='🔙 Назад',callback_data=f'вернуться_время_аренда_{str(msg).split("_")[2]}'))
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'🛎 Выбранный сервис: <b>{rent[1]}</b>\n⏳ Срок аренды: <b>{str(msg).split("_")[2]} ч.</b>',parse_mode='HTML',reply_markup=rent_buy)
				else:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="В данный момент номера для этого сервиса не доступны")


			if 'купить_аренда_' in str(msg):
				time.sleep(0.1)
				if call.message.chat.id not in last_time:
					last_time[call.message.chat.id] = time.time()
					buy_rent(call,msg)
				else:
					if (time.time() - last_time[call.message.chat.id]) * 1000 < 2000:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Между запросами должно пройти 2 сек.")
						bot.send_message('-1001270414760', f'Аренда\nПоказали пользователю <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> уведомление об ожидании 2 секунд между запросами',parse_mode='HTML')
						return 0
					else:
						last_time[call.message.chat.id] = time.time()
						buy_rent(call,msg)

			if str(msg)[:12] == 'номер_купить':
				try:
					connection,q = connect()
					bot.send_message('-1001270414760', msg)
					q.execute(f'SELECT code FROM ugc_service_all where id = "{str(msg)[12:]}"')
					row = q.fetchone()[0]
					try:
						bot.send_message(call.message.chat.id, texts.country_list(row,'1',call.message.chat.id),parse_mode='HTML',reply_markup=keyboards.country_list(row,'1',call.message.chat.id))
					except:
						pass
						# bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не получилось найти номер")
				except:
					# bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не получилось найти номер")
					pass

			if str(msg) == 'реклама_удалить':
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

			if 'купитьномер_' in str(msg):
				deposit_keyb = types.InlineKeyboardMarkup()
				deposit_keyb.add(types.InlineKeyboardButton(text='Купить',callback_data=f"подтверитьпокупку_{str(msg).split('_')[1]}_{str(msg).split('_')[2]}"))
				msgg = bot.send_message(call.message.chat.id,'Для подтверждения, нажмите на кнопку ниже',reply_markup=deposit_keyb)


			if 'подтверитьпокупку_' in str(msg):
				time.sleep(0.1)
				if call.message.chat.id not in last_time:
					last_time[call.message.chat.id] = time.time()
					buy_number(call,msg)
				else:
					if (time.time() - last_time[call.message.chat.id]) * 1000 < 2000:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Между запросами должно пройти 2 сек.")
						return 0
					else:
						last_time[call.message.chat.id] = time.time()
						buy_number(call,msg)





			if 'отменить_аренда_' in str(msg):
				connection,q = connect()
				q.execute(f'''SELECT * FROM ugc_rent_list where rentid = "{str(msg)[16:]}"''')
				ugc_phones = q.fetchone()
				if ugc_phones != None:
					if str(ugc_phones[6]) == '1':
						answer = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentStatus&id={str(msg).split("_")[2]}').json()
						if answer['status'] == 'success':
							q.execute(f"update ugc_rent_list set activ = '0' where rentid = '{msg[16:]}'")
							connection.commit()
							bot.send_message(call.message.chat.id, f'<b>Номер <code>{ugc_phones[4]}</code> отменен, но деньги не возвращены, ведь вы уже получили смс на номер</b>',parse_mode='HTML')
						elif answer['status'] == 'error':
							cancel = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=setRentStatus&id={str(msg).split("_")[2]}&status=2').json()
							if cancel['status'] == 'success':
								if answer['message'] == 'STATUS_FINISH':
									q.execute(f"update ugc_rent_list set activ = '0' where rentid = '{msg[16:]}'")
									connection.commit()
									bot.send_message(call.message.chat.id, f'<b>Номер <code>{ugc_phones[4]}</code> отменен, но деньги не возвращены, действие номера завершено</b>',parse_mode='HTML')
								elif answer['message'] == 'STATUS_CANCEL':
									q.execute(f"update ugc_rent_list set activ = '0' where rentid = '{msg[16:]}'")
									connection.commit()
									bot.send_message(call.message.chat.id, f'<b>Номер <code>{ugc_phones[4]}</code> отменен, но деньги не возвращены, действие номера завершено</b>',parse_mode='HTML')

								elif answer['message'] == 'STATUS_WAIT_CODE':
									q.execute(f"update ugc_rent_list set activ = '0' where rentid = '{msg[16:]}'")
									connection.commit()
									q.execute(f"update ugc_users set balance = balance + '{ugc_phones[5]}' where userid = '{ugc_phones[1]}'")
									connection.commit()
									bot.send_message(call.message.chat.id, f'<b>Номер <code>{ugc_phones[4]}</code> отменен, на баланс вернули {ugc_phones[5]} руб</b>',parse_mode='HTML')
							elif cancel['message'] == 'CANT_CANCEL':
								q.execute(f"update ugc_rent_list set activ = '0' where rentid = '{msg[16:]}'")
								connection.commit()
								bot.send_message(call.message.chat.id, f'<b>Номер <code>{ugc_phones[4]}</code> отменен, но деньги не возвращены, прошло 20 минут с момента покупки</b>',parse_mode='HTML')







			if 'отменить_смс_' in str(msg):
				try:
					connection,q = connect()
					q.execute(f'''SELECT site FROM ugc_phones where phone_id = "{str(msg).split('_')[2]}"''')
					site = q.fetchone()[0]
					q.execute(f'''SELECT * FROM ugc_phones where phone_id = "{str(msg).split('_')[2]}"''')
					ugc_phones = q.fetchone()
					if site == 'smshub':
						activation = GetStatus(
									id=str(msg).split('_')[2],
								).request(wrapper)
						if activation['status'] == 'STATUS_OK':
							deactivation = SetStatus(id=str(msg).split('_')[2],status='8').request(wrapper)
							q.execute(f"""update ugc_phones set sms = '0' where phone_id = '{str(msg).split('_')[2]}'""")
							connection.commit()
							bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер отменен")
							bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
						elif activation['status'] == 'STATUS_WAIT_CODE':
							if str(ugc_phones[4]) == '3':
								deactivation = SetStatus(id=str(msg).split('_')[2],status='8').request(wrapper)
								bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> нажал на отмену номера ({ugc_phones[2]}), сервис {ugc_phones[3]}\n{deactivation}',parse_mode='HTML')
								q.execute(f"""update ugc_phones set sms = '0' where phone_id = '{str(msg).split('_')[2]}'""")
								connection.commit()
								bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер отменен")
								bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
							else:
								deactivation = SetStatus(id=str(msg).split('_')[2],status='8').request(wrapper)
								bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> нажал на отмену номера ({ugc_phones[2]}), сервис {ugc_phones[3]}\n{deactivation}',parse_mode='HTML')
								bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер отменен, деньги возвращены")
								q.execute(f"""update ugc_statistika set summa_phones = summa_phones - '{float(str(msg).split("_")[3]) - float(ugc_phones[5])}'""")
								connection.commit()
								q.execute(f"""update ugc_users set balance = balance + '{str(msg).split("_")[3]}' where userid = '{call.message.chat.id}'""")
								connection.commit()
								q.execute(f"""update ugc_phones set sms = '0' where phone_id = '{str(msg).split('_')[2]}'""")
								connection.commit()
								bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
						else:
							bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Номер недоступен")
							bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
					else:
						answer = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getStatus&id={str(msg).split("_")[2]}')
						if answer.text == 'STATUS_OK':
							deactivation = requests.get(url=f"https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=setStatus&status=8&id={str(msg).split('_')[2]}")
							q.execute(f"""update ugc_phones set sms = '0' where phone_id = '{str(msg).split('_')[2]}'""")
							connection.commit()
							bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер отменен")
							bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
						elif answer.text == 'STATUS_WAIT_CODE':
							if str(ugc_phones[4]) == '3':
								deactivation = requests.get(url=f"https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=setStatus&status=8&id={str(msg).split('_')[2]}")
								bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер отменен")
								bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
							else:
								deactivation = requests.get(url=f"https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=setStatus&status=8&id={str(msg).split('_')[2]}")
								bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер отменен, деньги возвращены")
								q.execute(f"""update ugc_statistika set summa_phones = summa_phones - '{float(str(msg).split("_")[3]) - float(ugc_phones[5])}'""")
								connection.commit()
								q.execute(f"""update ugc_users set balance = balance + '{str(msg).split("_")[3]}' where userid = '{call.message.chat.id}'""")
								connection.commit()
								q.execute(f"""update ugc_phones set sms = '0' where phone_id = '{str(msg).split('_')[2]}'""")
								connection.commit()
								bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
						else:
							bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Номер недоступен")
							bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				except:
					bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)


	except Exception as e:
		if 'Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message text is empty' not in traceback.format_exc():
			if 'Telegram API was unsuccessful. Error code: 400. Description: Bad Request: message to delete not found' not in traceback.format_exc():
				if 'Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message' not in traceback.format_exc():
					bot.send_message(825416463,traceback.format_exc())


def send_photoorno(message):
	global text_send_all
	global json_entit
	text_send_all = message.text
	json_entit = None
	if 'entities' in message.json:
		json_entit = message.json['entities']
	msg = bot.send_message(message.chat.id, '<b>Введите нужны аргументы в таком виде:\n\nНазвание рекламы\nСсылка на картинку\nКогда отправить</b>\n\nЕсли что-то из этого не нужно, то напишите "Нет", указывайте дату в таком формате: год-месяц-число часы:минуты (пример: 2020-12-09 15:34)',parse_mode='HTML')
	bot.register_next_step_handler(msg, admin_send_message_all_text_rus)

def admin_send_message_all_text_rus(message):
	# try:
		global photoo
		global keyboar
		global time_send
		global v
		time_send = message.text.split('\n')[2]
		photoo = message.text.split('\n')[1]
		keyboar = message.text.split('\n')[0]
		v = 0
		if str(photoo.lower()) != 'Нет'.lower():
			v = v+1
			
		if str(keyboar.lower()) != 'Нет'.lower():
			v = v+2

		if v == 0:
			msg = bot.send_message(message.chat.id,  text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
		
		elif v == 1:
			msg = bot.send_photo(message.chat.id,str(photoo),  text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		elif v == 2:
			msg = bot.send_message(message.chat.id,  text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		elif v == 3:
			msg = bot.send_photo(message.chat.id,str(photoo),  text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
	# except:
	# 	bot.send_message(message.chat.id, "Ошибка при вводе аргументов",parse_mode='HTML')

def admin_send_message_all_text_da_rus(message):
	otvet = message.text
	colvo_send_message_users = 0
	colvo_dont_send_message_users = 0
	if message.text.lower() == 'Да'.lower():
		if time_send.lower() == 'нет':
			bot.send_message(message.chat.id, f'<b>Создайте рассылку заново, но прибавив к текущему времени 2-3 минуты</b>',parse_mode='HTML')
				# except:
				# 	bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))
		else:
			connection,q = connect()
			
			q.execute("INSERT INTO ugc_temp_sending (text,image,button,date) VALUES ('%s','%s','%s','%s')"%(text_send_all,photoo,keyboar,time_send))
			connection.commit()
			q.execute('update ugc_temp_sending set entit = "{}" where date = "{}"'.format(json_entit, time_send))
			connection.commit()
			bot.send_message(message.chat.id, f'<b>Успешно запланировали рассылку <code>{time_send}</code></b>',parse_mode='HTML')

def buy_rent(call,msg):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{call.message.chat.id}"')
	row = q.fetchone()
	q.execute(f'SELECT * FROM ugc_country WHERE id = "{row[3]}"')
	country = '0'
	response = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentServicesAndCountries&rent_time={str(msg).split("_")[3]}&country={country}').json()
	am = response['services'][str(msg).split("_")[2]]['quant']
	if response['services'][str(msg).split("_")[2]]['quant'] != 0:
		q.execute(f'SELECT * FROM asd WHERE da = "{str(msg).split("_")[2]}"')
		rent = q.fetchone()
		price = str(msg).split('_')[4]
		amn = float(price)
		if float(row[2]) >= float(amn):
			operators = ["beeline", "matrix", "megafon", "motiv", "mts", "rostelecom", "sber", "simsim", "tele2", "tinkoff", "winmobile", "yota"]
			get_phone = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentNumber&service={str(msg).split("_")[2]}&rent_time={str(msg).split("_")[3]}&country={country}').json()
			if get_phone['status'] == 'success':
				q.execute(f"""update ugc_users set balance = balance - '{"%.2f" % (float(price))}' where userid = """ + str(call.message.chat.id))
				connection.commit()
				now = datetime.datetime.now()
				bot.send_message('-1001270414760', f'#Аренда\nПользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> арендовал номер ({get_phone["phone"]["number"]}), сервис: {rent[0]}\n{get_phone}',parse_mode='HTML')
				bot.send_message(config.chat_new_phone, f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> арендовал номер ({get_phone["phone"]["number"]}), сервис: {rent[0]}',parse_mode='HTML')
				q.execute("INSERT INTO ugc_rent_list (userid,name,rentid,phone,price,data_start,data_end) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(call.message.chat.id,rent[0],get_phone['phone']['id'],get_phone['phone']['number'],price,now.strftime("%Y-%m-%d %H:%M:%S"),get_phone['phone']['endDate']))
				connection.commit()
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = texts.rent_text(call.message.chat.id,get_phone['phone']['id']),parse_mode='HTML')
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не нашли номер")
		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Баланса не хватает")
	else:
		bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не получилось найти номер")

def buy_number(call, msg):
	# if (time.time() - last_time[call.message.chat.id]) * 1000 < 2000:
	# 	bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Между запросами должно пройти 2 сек.")
	# 	return 0
	# else:
	# 	last_time[call.message.chat.id] = time.time()
	connection,q = connect()
	service = str(msg).split('_')[1]
	country = str(msg).split('_')[2]
	q.execute(f'SELECT * FROM ugc_users where userid = "{call.message.chat.id}"')
	user_infa = q.fetchone()
	q.execute(f'SELECT id FROM ugc_country where idd = "{country}"')
	countr_idd = q.fetchone()
	q.execute(f'SELECT * FROM ugc_service_all where code = "{service}" and country = "{countr_idd[0]}"')
	service_info = q.fetchone()
	now = datetime.datetime.now()
	if service_info[6] == 'smshub':
		if float(service_info[4]) <= float(user_infa[2]):
			# try:
				buy_number = types.InlineKeyboardMarkup()
				buy_number.add(types.InlineKeyboardButton(text='📋 Меню',callback_data=f'вернуться_назад'))
				q.execute(f'SELECT idd FROM ugc_country where id = "{service_info[3]}"')
				countr_idd = q.fetchone()
				q.execute(f"update ugc_users set balance = balance - '{service_info[4]}' where userid = " + str(call.message.chat.id))
				connection.commit()
				if str(service_info[3]) == 'russia':
					operators = ["beeline", "matrix", "megafon", "motiv", "mts", "rostelecom", "sber", "simsim", "tele2", "tinkoff", "winmobile", "yota"]
					activation = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getNumber&service={service}&operator={random.choice(operators)}&country={countr_idd[0]}')
				else:
					activation = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getNumber&service={service}&country={countr_idd[0]}')
				if 'ACCESS_NUMBER' in activation.text:
					print(activation.text)
					bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер с сервиса смсхаб ({activation.text.split(":")[2]}), сервис: {service_info[1]}\n{activation.text}',parse_mode='HTML')
					bot.send_message(config.chat_new_phone, f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер ({activation.text.split(":")[2]}), сервис: {service_info[1]}',parse_mode='HTML')
					check = types.InlineKeyboardMarkup()
					check.add(types.InlineKeyboardButton(text='✖️ Отменить',callback_data=f"отменить_смс_{activation.text.split(':')[1]}_{service_info[4]}"))
					q.execute("INSERT INTO ugc_phones (userid,nubmer,service,price,phone_id,site,sms,date_get) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(call.message.chat.id,activation.text.split(':')[2],service_info[1],service_info[4],activation.text.split(':')[1],'smshub','2',now.strftime("%Y-%m-%d %H:%M:%S")))
					connection.commit()

					bot.send_message(call.message.chat.id, f'''❤️ Сервис: {service_info[1]}
📱 Ваш номер: <code>{activation.text.split(':')[2]}</code>
Ожидайте прихода смс

Если смс не прийдет через 5 минут, то вам вернуться потраченные деньги за этот номер, аренда номера будет отменена!!!''',parse_mode='HTML',reply_markup=check)

				elif 'NO_NUMBERS' in activation.text:
					activation_two = requests.get(url=f"https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getNumber&service={service}&country={countr_idd[0]}")
					print(activation_two.text)
					bot.send_message('-1001270414760', f'Пользователь хотел купить номер, но на смсхаб нет, идем на smsactivate: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>, сервис: {service_info[1]}\n{activation.text}',parse_mode='HTML')
					if activation_two.text == 'NO_NUMBERS' or activation_two.text == 'NO_BALANCE':
						q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
						connection.commit()
						bot.send_message('-1001270414760', f'Пользователь хотел купить номер, но номеров нигде нет: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>, сервис: {service_info[1]}\n{activation_two.text}',parse_mode='HTML')
						bot.send_message(call.message.chat.id, 'На данный момент номеров нет, ожидайте пополнения!')
					elif 'ACCESS_NUMBER' in activation_two.text:
						bot.send_message(config.chat_new_phone, f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер ({activation_two.text.split(":")[2]}), сервис: {service_info[1]}',parse_mode='HTML')
						check = types.InlineKeyboardMarkup()
						bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер с сервиса smsactivate ({activation_two.text.split(":")[2]}), сервис: {service_info[1]}\n{activation_two.text}',parse_mode='HTML')
						check.add(types.InlineKeyboardButton(text='✖️ Отменить',callback_data=f"отменить_смс_{activation_two.text.split(':')[1]}_{service_info[4]}"))
						q.execute("INSERT INTO ugc_phones (userid,nubmer,service,price,phone_id,site,sms,date_get) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(call.message.chat.id,activation_two.text.split(':')[2],service_info[1],service_info[4],activation_two.text.split(':')[1],'smsactivate','2',now.strftime("%Y-%m-%d %H:%M:%S")))
						connection.commit()
						bot.send_message(call.message.chat.id, f'''❤️ Сервис: {service_info[1]}
📱 Ваш номер: <code>{activation_two.text.split(':')[2]}</code>
Ожидайте прихода смс

Если смс не прийдет через 5 минут, то вам вернуться потраченные деньги за этот номер, аренда номера будет отменена!!!''',parse_mode='HTML',reply_markup=check)
					else:
						if activation_two.text == 'NO_BALANCE':
							bot.send_message(config.chat_new_phone, f'Пополните баланс на сайте',parse_mode='HTML')
							bot.send_message('-1001270414760', f'Пополните баланс на сайте, пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML')
						q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
						connection.commit()
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Произошла ошибка, повторите попытку позже")

				else:
					if activation.text == 'NO_BALANCE':
						bot.send_message(config.chat_new_phone, f'Пополните баланс на сайте',parse_mode='HTML')
						bot.send_message('-1001270414760', f'Пополните баланс на сайте, пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML')
					q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
					connection.commit()
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Произошла ошибка, повторите попытку позже")


			# except:
			# 	q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
			# 	connection.commit()
			# 	bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="В данный момент номера для этого сервиса не доступны")
		else:
			bot.send_message('-1001270414760', f'Пользователю не хватило баланса: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML')
			bot.send_message(call.message.chat.id,'Баланса не хватает')

	else:
		if float(service_info[4]) <= float(user_infa[2]):
			try:
				buy_number = types.InlineKeyboardMarkup()
				# buy_number.add(types.InlineKeyboardButton(text='🔁 Повторить заказ',callback_data=f'купить_номер_{str(msg)[13:]}'))
				buy_number.add(types.InlineKeyboardButton(text='📋 Меню',callback_data=f'вернуться_назад'))
				q.execute(f'SELECT idd FROM ugc_country where id = "{service_info[3]}"')
				countr_idd = q.fetchone()
				q.execute(f"update ugc_users set balance = balance - '{service_info[4]}' where userid = " + str(call.message.chat.id))
				connection.commit()
				# activation = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getNumber&service={service}&country={countr_idd[0]}')
				activation = requests.get(url=f"https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getNumber&service={service}&country={countr_idd[0]}")
				if 'ACCESS_NUMBER' in activation.text:
					print(activation.text)
					bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер с сервиса smsactivate({activation.text.split(":")[2]}), сервис: {service_info[1]}\n{activation.text}',parse_mode='HTML')
					bot.send_message(config.chat_new_phone, f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер ({activation.text.split(":")[2]}), сервис: {service_info[1]}',parse_mode='HTML')
					check = types.InlineKeyboardMarkup()
					check.add(types.InlineKeyboardButton(text='✖️ Отменить',callback_data=f"отменить_смс_{activation.text.split(':')[1]}_{service_info[4]}"))
					q.execute("INSERT INTO ugc_phones (userid,nubmer,service,price,phone_id,site,sms,date_get) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(call.message.chat.id,activation.text.split(':')[2],service_info[1],service_info[4],activation.text.split(':')[1],'smsactivate','2',now.strftime("%Y-%m-%d %H:%M:%S")))
					connection.commit()
					bot.send_message(call.message.chat.id, f'''❤️ Сервис: {service_info[1]}
📱 Ваш номер: <code>{activation.text.split(':')[2]}</code>
Ожидайте прихода смс

Если смс не прийдет через 5 минут, то вам вернуться потраченные деньги за этот номер, аренда номера будет отменена!!!''',parse_mode='HTML',reply_markup=check)

				elif 'NO_NUMBERS' in activation.text or activation.text == 'NO_BALANCE':
					if str(service_info[3]) == 'russia':
						operators = ["beeline", "matrix", "megafon", "motiv", "mts", "rostelecom", "sber", "simsim", "tele2", "tinkoff", "winmobile", "yota"]
						activation_two = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getNumber&service={service}&operator={random.choice(operators)}&country={countr_idd[0]}')
					else:
						activation_two = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getNumber&service={service}&country={countr_idd[0]}')
					print(activation_two.text)
					if activation_two.text == 'NO_NUMBERS':
						bot.send_message('-1001270414760', f'Пользователь хотел купить номер его нигде нет: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> {activation_two.text}',parse_mode='HTML')
						q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
						connection.commit()
						bot.send_message(call.message.chat.id, 'На данный момент номеров нет, ожидайте пополнения!')
					elif 'ACCESS_NUMBER' in activation_two.text:
						bot.send_message(config.chat_new_phone, f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер ({activation_two.text.split(":")[2]}), сервис: {service_info[1]}',parse_mode='HTML')
						check = types.InlineKeyboardMarkup()
						check.add(types.InlineKeyboardButton(text='✖️ Отменить',callback_data=f"отменить_смс_{activation_two.text.split(':')[1]}_{service_info[4]}"))
						q.execute("INSERT INTO ugc_phones (userid,nubmer,service,price,phone_id,site,sms,date_get) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(call.message.chat.id,activation_two.text.split(':')[2],service_info[1],service_info[4],activation_two.text.split(':')[1],'smshub','2',now.strftime("%Y-%m-%d %H:%M:%S")))
						connection.commit()
						bot.send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> купил номер с смсхаб ({activation_two.text.split(":")[2]}), сервис: {service_info[1]}\n{activation_two.text}',parse_mode='HTML')
						bot.send_message(call.message.chat.id, f'''❤️ Сервис: {service_info[1]}
📱 Ваш номер: <code>{activation_two.text.split(':')[2]}</code>
Ожидайте прихода смс

Если смс не прийдет через 5 минут, то вам вернуться потраченные деньги за этот номер, аренда номера будет отменена!!!''',parse_mode='HTML',reply_markup=check)
					else:
						if activation_two.text == 'NO_BALANCE':
							bot.send_message(config.chat_new_phone, f'Пополните баланс на сайте',parse_mode='HTML')
							bot.send_message('-1001270414760', f'Пополните баланс на сайте, пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML')
						q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
						connection.commit()
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Произошла ошибка, повторите попытку позже")

				else:
					if activation.text == 'NO_BALANCE':
						bot.send_message(config.chat_new_phone, f'Пополните баланс на сайте',parse_mode='HTML')
						bot.send_message('-1001270414760', f'Пополните баланс на сайте, пользователь: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML')
					q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
					connection.commit()
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Произошла ошибка, повторите попытку позже")


			except:
				q.execute(f"update ugc_users set balance = balance + '{service_info[4]}' where userid = " + str(call.message.chat.id))
				connection.commit()
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="В данный момент номера для этого сервиса не доступны")
		else:
			bot.send_message(call.message.chat.id,'Баланса не хватает')




bot.polling(none_stop=True)