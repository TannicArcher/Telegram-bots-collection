import telebot
from telebot import types
import sqlite3
from smshuborg import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber, SetStatus, GetStatus,GetFreeSlotsAndPrices,ServiceStorage
import requests
import config
import json
from tools.mysql import connect


def main():
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_ads_button')
	rent_infa = q.fetchall()
	main_menu = telebot.types.ReplyKeyboardMarkup(True)
	main_menu.row('🔥 Номера','💣 Аренда')
	main_menu.row('🌺 Мультисервис')
	main_menu.row('👤 Профиль','ℹ️ INFO')
	for i in rent_infa:
		main_menu.row(str(i[1]))
	return main_menu


def rent_spisok_time(service):
	try:
		connection,q = connect()
		
		q.execute(f'SELECT code FROM ugc_service_all where id = "{service}"')
		row = q.fetchone()[0]
		answer = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentServicesAndCountries&rent_time=4&country=0').json()
		hour4 = float(answer['services'][str(row)]['cost']) + float(answer['services'][str(row)]['cost']  / 100 * 15)
		answer = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentServicesAndCountries&rent_time=24&country=0').json()
		hour24 = float(answer['services'][str(row)]['cost']) + float(answer['services'][str(row)]['cost']  / 100 * 15)
		answer = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentServicesAndCountries&rent_time=168&country=0').json()
		hour168 = float(answer['services'][str(row)]['cost']) + float(answer['services'][str(row)]['cost']  / 100 * 15)
		rent_spisok = types.InlineKeyboardMarkup(row_width=2)
		rent_spisok.add(types.InlineKeyboardButton(text=f'🕐 4 часа | {"%.2f" % hour4} ₽',callback_data=f'аренда_время_4_{row}_{"%.2f" % hour4}'),types.InlineKeyboardButton(text=f'🕐 24 часа | {"%.2f" % hour24} ₽',callback_data=f'аренда_время_24_{row}_{"%.2f" % hour24}'))
		rent_spisok.add(types.InlineKeyboardButton(text=f'🕐 7 дней | {"%.2f" % hour168} ₽',callback_data=f'аренда_время_168_{row}_{"%.2f" % hour168}'))
		rent_spisok.add(types.InlineKeyboardButton(text='🔙',callback_data=f'вернуться_сервисы_аренда_{service}'))
		return rent_spisok
	except:
		return 'Не удалось найти номер'
	

def rent_activ(userid):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_rent_list where userid = "{userid}" and activ = "1"')
	row = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=2)
	btns = []
	for i in range(len(row)):
		try:
			btns.append(types.InlineKeyboardButton(text=f'{row[i][2]} | {row[i][4]}',callback_data=f'история_аренда{row[i][3]}'))
				
		except:
			continue
	while btns != []:
		try:
			services.add(
				btns[0],
				btns[1],
				)
			del btns[1], btns[0]
		except:
			services.add(btns[0])
			del btns[0]
	return services




deposit_keyb = types.InlineKeyboardMarkup()
deposit_keyb.add(types.InlineKeyboardButton(text='QIWI',callback_data=f'пополнить_баланс_qiwi'))
deposit_keyb.add(types.InlineKeyboardButton(text='BANKER',callback_data=f'пополнить_баланс_btc'),types.InlineKeyboardButton(text='ChatEx',callback_data=f'пополнить_баланс_chatex'))

back_to_start = types.InlineKeyboardMarkup()
back_to_start.add(types.InlineKeyboardButton(text='🔙 Назад',callback_data=f'вернуться_назад'))

back_to_menu = types.InlineKeyboardMarkup()
back_to_menu.add(types.InlineKeyboardButton(text='🔙 Вернуться в меню',callback_data=f'вернуться_в_меню'))


soglasen = types.InlineKeyboardMarkup()
soglasen.add(types.InlineKeyboardButton(text='✅ Согласен',callback_data=f'согласен_правила'))


referal = types.InlineKeyboardMarkup()
referal.add(types.InlineKeyboardButton(text='Вывод средств',callback_data=f'вывести_средства'))
referal.add(types.InlineKeyboardButton(text='🔙 Назад',callback_data=f'вернуться_назад'))


def country_list():
	try:
		connection,q = connect()
		q.execute(f'SELECT * FROM ugc_country')
		row = q.fetchall()
		services = types.InlineKeyboardMarkup(row_width=3)
		btns = []
		for i in range(len(row)):
			try:
				btns.append(types.InlineKeyboardButton(text=f'{row[i][1]}',callback_data=f'Изменить_страна_{row[i][0]}'))
					
			except:
				continue
		while btns != []:
			try:
				services.add(
					btns[0],
					btns[1],
					btns[2]
					)
				del btns[2],btns[1], btns[0]
			except:
				services.add(btns[0])
				del btns[0]
		services.add(types.InlineKeyboardButton(text='🔙 Назад',callback_data=f'вернуться_назад'))
		return services
	except:
		pass

info = types.InlineKeyboardMarkup()
info.add(types.InlineKeyboardButton(text='📞 Связаться с поддержкой ',url='t.me/HelperSMS_sup'))
info.add(types.InlineKeyboardButton(text='✉️ Правила сервиса',callback_data='правила'))
info.add(types.InlineKeyboardButton(text='🤖 Новости бота',url='t.me/News_Helpera'),types.InlineKeyboardButton(text='🤡 Мемный скам',url='https://t.me/joinchat/AAAAAE10Xa-30sJMLnSyOw'))
info.add(types.InlineKeyboardButton(text='🔙 Назад',callback_data=f'вернуться_назад'))

profile = types.InlineKeyboardMarkup()
profile.add(types.InlineKeyboardButton(text='💸 Пополнить баланс',callback_data=f'пополнить_баланс'))
profile.add(types.InlineKeyboardButton(text='👥 Реферальная сеть',callback_data=f'мои_рефералы'))


rent_menu = types.InlineKeyboardMarkup()
rent_menu.add(types.InlineKeyboardButton(text='❕ Арендовать',callback_data=f'аренда'),types.InlineKeyboardButton(text='❕ История',callback_data=f'история_аренда'))	

mult_menu = types.InlineKeyboardMarkup()
mult_menu.add(types.InlineKeyboardButton(text='❕ Арендовать',callback_data=f'мульт'))	

def rent_list():
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_service_all where rent = "1"')
	row = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=3)
	btns = []
	# answer = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getPrices&country=0').json()
	for i in row:
		# print(answer)
		# price = float(answer["0"][str(i[2])]["cost"]) + (answer["0"][str(i[2])]["cost"] / 100 * 10)
		btns.append(types.InlineKeyboardButton(text=f'{i[1]}',callback_data=f'аренда_купить{i[0]}'))
	while btns != []:
		try:
			services.add(
				btns[0],
				btns[1],
				btns[2],
				)
			del btns[0],btns[0], btns[0]
			
		except:
			services.add(btns[0])
			del btns[0]
	services.add(types.InlineKeyboardButton(text='🔙',callback_data=f'вернуться_аренда'))
	return services


def mult_list(message):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_mult_service')
	row = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=3)
	btns = []
	amd = 0
	for i in row:
		btns.append(types.InlineKeyboardButton(text=f'{i[1] if i[2] not in message else f"✅ {i[1]}"} | {i[3]} ₽',callback_data=f'{message}:{i[2]}'))
		if i[2] in message:
			amd += 1
	while btns != []:
		try:
			services.add(
				btns[0],
				btns[1],
				btns[2],
				)
			del btns[0],btns[0], btns[0]
			
		except:
			services.add(btns[0])
			del btns[0]
	if amd != 0:
		services.add(types.InlineKeyboardButton(text=f'🧸 Заказать',callback_data=f'купитьмулт{message.replace("мульт","")}'))
	services.add(types.InlineKeyboardButton(text='🔙',callback_data=f'вернуться_му'))
	return services





def services_list():
	# try:
		connection,q = connect()
		
		q.execute(f'SELECT * FROM ugc_service_all where spisok = "1"')
		row = q.fetchall()

		services = types.InlineKeyboardMarkup(row_width=3)
		btns = []
		btns_len = []
		for i in row:
			try:
			# q.execute(f'SELECT price FROM ugc_service_all where code = "{i[2]}" and price != "0" ORDER BY price DESC')
				# q.execute(f'SELECT price FROM ugc_service_all where code = "{i[2]}" and price != "0" ORDER BY price ASC')
				# roww = q.fetchone()[0]
				btns.append(types.InlineKeyboardButton(text=f'{i[1]}',callback_data=f'номер_купить{i[0]}'))
			except:
				continue

		while btns != []:
			try:
				services.add(
					btns[0],
					btns[1],
					btns[2],
					)
				del btns[0],btns[0], btns[0]
				
			except:
				services.add(btns[0])
				del btns[0]

		services.add(types.InlineKeyboardButton(text='Выйти',callback_data=f'вернуться_назад'))
		return services
	# except:
	# 	return 'Сервисы недоступны'




def country_list(service, tt,userid):
	try:
		connection,q = connect()
		
		if tt == '1':
			q.execute(f'SELECT balance FROM ugc_users where userid = "{userid}"')
			balance = q.fetchone()[0]
			q.execute(f'SELECT * FROM ugc_service_all where code = "{service}" and spisok = "1"')
			row_site = q.fetchone()
			services = types.InlineKeyboardMarkup(row_width=2)
			if row_site[6] == 'smshub':
				print(f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getPrices&service={service}')
				try:
					response = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getPrices&service={service}').json()
					q.execute(f'SELECT * FROM ugc_country')
					row_sitee = q.fetchall()
					for i in row_sitee:
						try:
							amm = i[2]
							answer = response[str(amm)]
							if len(answer) != 0:
								text = response[str(amm)][str(service)]
								for colvo in text:
									price = response[str(amm)][str(service)][str(colvo)]
									q.execute(f'SELECT price FROM ugc_service_all where code = "{service}" and country = "{i[0]}" and price != "0"')
									row_price = q.fetchone()[0]
									q.execute(f'SELECT name FROM ugc_country where idd = "{amm}"')
									row = q.fetchone()[0]
									services.add(types.InlineKeyboardButton(text=f'{row} | {float(row_price)} ₽',callback_data=f'купитьномер_{service}_{amm}'))		
									break
						except:
							continue
				except:
					response = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getPrices&service={service}').json()
					q.execute(f'SELECT * FROM ugc_country')
					row_sitee = q.fetchall()
					for i in row_sitee:
						try:
							amm = i[2]
							answer = response[str(amm)][str(service)]
							if int(answer['count']) > 0:
								q.execute(f'SELECT price FROM ugc_service_all where code = "{service}" and country = "{i[0]}" and price != "0"')
								row_price = q.fetchone()[0]
								text = response[str(amm)][str(service)]['count']
								price = response[str(amm)][str(service)]['cost']
								q.execute(f'SELECT name FROM ugc_country where idd = "{amm}"')
								row = q.fetchone()[0]
								services.add(types.InlineKeyboardButton(text=f'{row} | {float(row_price)} ₽',callback_data=f'купитьномер_{service}_{amm}'))
						except:						
							continue
			else:
				response = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getPrices&service={service}').json()
				q.execute(f'SELECT * FROM ugc_country')
				row_sitee = q.fetchall()
				for i in row_sitee:
					try:
						amm = i[2]
						answer = response[str(amm)][str(service)]
						if int(answer['count']) > 0:
							q.execute(f'SELECT price FROM ugc_service_all where code = "{service}" and country = "{i[0]}" and price != "0"')
							row_price = q.fetchone()[0]
							text = response[str(amm)][str(service)]['count']
							price = response[str(amm)][str(service)]['cost']
							q.execute(f'SELECT name FROM ugc_country where idd = "{amm}"')
							row = q.fetchone()[0]
							services.add(types.InlineKeyboardButton(text=f'{row} | {float(row_price)} ₽',callback_data=f'купитьномер_{service}_{amm}'))
					except:						
						continue
			return services
	except:
		pass








		

# def services_list():
# 	try:
# 		connection,q = connect()
# 		
# 		q.execute(f'SELECT * FROM ugc_service_all')
# 		row = q.fetchall()
# 		return services


