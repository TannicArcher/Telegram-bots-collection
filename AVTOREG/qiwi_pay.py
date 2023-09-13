# -*- coding: utf-8 -*- 
import telebot
from telebot import types,apihelper
from light_qiwi import Qiwi, OperationType
import sqlite3
import datetime
import config
from tools.mysql import connect

api = Qiwi(config.qiwi_token, config.qiwi_number)
@api.bind_check(operation=OperationType.ALL)
def waiter(payment):
	if payment.type == OperationType.IN:
		connection,q = connect()
		q.execute('SELECT id FROM ugc_pays WHERE pay_id = ' + str(payment.raw['txnId']))
		temp_pay = q.fetchone()
		if 'RUB' in str(payment.currency) and temp_pay == None and float(payment.amount) >= 1:
			now = datetime.datetime.now()
			nnow = str(now)[:19]
			q.execute("INSERT INTO ugc_pays (pay_id,userid,date_pay,summa) VALUES ('%s','%s','%s','%s')"%(payment.raw['txnId'],payment.comment,nnow,payment.total))
			connection.commit()
			q.execute(f"update ugc_users set balance = balance + '{payment.total}' where userid = '{payment.comment}'")
			connection.commit()
			try:
				q.execute(f'SELECT ref1 FROM ugc_users WHERE userid = "{payment.comment}"')
				ref1 = q.fetchone()
				if str(ref1[0]) != '0':
					addd = float(payment.total) /100 * 15
					q.execute(f"update ugc_users set balance = balance + '{addd}' where userid = '{ref1}'")
					connection.commit()
				try:
					q.execute(f"update ugc_statistika set deposit_summa = deposit_summa + '{payment.total}'")
					connection.commit()
					telebot.TeleBot(config.token).send_message(payment.comment, f'💎 На ваш баланс зачислено {payment.total} RUB')
					telebot.TeleBot(config.token).send_message(config.chat_new_user, f'Пользователь: <a href="tg://user?id={payment.comment}">{payment.comment}</a>\nПополнил баланс на {payment.total} руб через QIWI\nДата: {nnow}',parse_mode='HTML')
					telebot.TeleBot(config.token).send_message('-1001270414760', f'Пользователь: <a href="tg://user?id={payment.comment}">{payment.comment}</a>\nПополнил баланс на {payment.total} руб через QIWI\nДата: {nnow}',parse_mode='HTML')
				except:
					pass
			except:
				pass

api.start()