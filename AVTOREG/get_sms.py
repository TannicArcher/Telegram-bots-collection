# -*- coding: utf-8 -*- 
import telebot
from telebot import types,apihelper
import requests
import json
import sqlite3
import time
from tools.mysql import connect
from datetime import datetime, timedelta
import config



while True:
	try:
		connection,q = connect()
		q.execute(f'''SELECT * FROM ugc_phones where sms = "2" or sms = "3"''')
		ugc_phones = q.fetchall()
		for i in ugc_phones:
			time.sleep(0.2)
			if i[7] == 'smshub':
				date = datetime.strptime(i[8], "%Y-%m-%d %H:%M:%S")
				now = str(datetime.now())[:19]
				norm_date = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
				date_answer = norm_date - date
				if int(str(date_answer).split(':')[1]) > 5 and str(i[4]) == "2":
					q.execute(f"update ugc_phones set sms = '0' where phone_id = '{i[6]}'")
					connection.commit()
					q.execute(f"update ugc_users set balance = balance + '{i[5]}' where userid = '{i[1]}'")
					connection.commit()
					edit_status = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=setStatus&status=8&id={i[6]}')
					# try:
					bot = telebot.TeleBot(config.token).send_message(i[1], f'<b>Код для номера <code>{i[2]}</code> не пришел, вам будут возвращены деньги</b>',parse_mode='html')
					bot = telebot.TeleBot(config.token).send_message('-1001270414760', f'<b>Код для номера <code>{i[2]}</code> не пришел, пользователю вернулись {i[5]} RUB',parse_mode='HTML')
					# except:
					# 	continue
				else:
					response = requests.get(url=f"https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=getStatus&id={i[6]}")
					print(f'{response.text} - {i[2]}')
					if response.text == 'STATUS_WAIT_CODE':
						pass
					elif 'STATUS_OK' in response.text:
						edit_status = requests.get(url=f'https://smshub.org/stubs/handler_api.php?api_key={config.token_sms}&action=setStatus&status=3&id={i[6]}')
						q.execute(f"update ugc_phones set sms = '3' where phone_id = '{i[6]}'")
						connection.commit()
						try:
							bot = telebot.TeleBot(config.token).send_message(i[1], f'<b>Номер: <code>{i[2]}</code>\nСерис: <code>{i[3]}</code>\nСмс: <code>{response.text.split(":")[1]}</code></b>',parse_mode='html')
							bot = telebot.TeleBot(config.token).send_message('-1001270414760', f'<b>Новое смс\nПользователь:{i[1]}\nНомер: <code>{i[2]}</code>\nСерис: <code>{i[3]}</code>\nСмс: <code>{response.text.split(":")[1]}</code></b>',parse_mode='HTML')
						except:
							continue

					elif 'STATUS_CANCEL' in response.text:
						q.execute(f"update ugc_phones set sms = '1' where phone_id = '{i[6]}'")
						connection.commit()
			else:
				date = datetime.strptime(i[8], "%Y-%m-%d %H:%M:%S")
				now = str(datetime.now())[:19]
				norm_date = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
				date_answer = norm_date - date
				if int(str(date_answer).split(':')[1]) >= 5 and str(i[4]) == "2":
					q.execute(f"update ugc_phones set sms = '0' where phone_id = '{i[6]}'")
					connection.commit()
					q.execute(f"update ugc_users set balance = balance + '{i[5]}' where userid = '{i[1]}'")
					connection.commit()
					edit_status = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=setStatus&status=8&id={i[6]}')
					# try:
					bot = telebot.TeleBot(config.token).send_message(i[1], f'<b>Код для номера <code>{i[2]}</code> не пришел, вам будут возвращены деньги</b>',parse_mode='html')
					bot = telebot.TeleBot(config.token).send_message('-1001270414760', f'<b>Код для номера <code>{i[2]}</code> не пришел, пользователю вернулись {i[5]} RUB',parse_mode='HTML')
					# except:
					# 	continue
				else:
					response = requests.get(url=f"https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getStatus&id={i[6]}")
					print(f'{response.text} - {i[2]}')
					if response.text == 'STATUS_WAIT':
						pass
					elif 'STATUS_OK' in response.text:
			
						edit_status = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=setStatus&status=3&id={i[6]}')
						print(edit_status.text)
						q.execute(f"update ugc_phones set sms = '3' where phone_id = '{i[6]}'")
						connection.commit()
						try:
							bot = telebot.TeleBot(config.token).send_message(i[1], f'<b>Номер: <code>{i[2]}</code>\nСерис: <code>{i[3]}</code>\nСмс: <code>{response.text.split(":")[1]}</code></b>',parse_mode='html')
							bot = telebot.TeleBot(config.token).send_message('-1001270414760', f'<b>Новое смс\nПользователь:{i[1]}\nНомер: <code>{i[2]}</code>\nСерис: <code>{i[3]}</code>\nСмс: <code>{response.text.split(":")[1]}</code></b>',parse_mode='HTML')
						except:
							continue

					elif 'STATUS_CANCEL' in response.text:
						q.execute(f"update ugc_phones set sms = '1' where phone_id = '{i[6]}'")
						connection.commit()		
	except:
		continue

