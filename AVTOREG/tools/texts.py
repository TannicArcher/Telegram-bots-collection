import telebot
from telebot import types,apihelper
import keyboards
import config
import sqlite3
import requests
import datetime
import json
from tools.mysql import connect

	


text_faq = '''<b>ПО ВСЕМ ВОПРОСАМ 
ПИСАТЬ @alxkks</b>
'''

info = """Пользовательское соглашение
1. Порядок проведения активации следующий:
- 1.1. Нажать на кнопку "номера", выбрать необходимый сервис
- 1.2  Нажать на кнопку "страна", выбрать необходимую страну
- 1.3  Нажать на кнопку "Получить смс", далее у вас появится номер
- 1.4  Дождаться поступления смс и отображения его содержания
- 1.5  Если вам необходимо получить больше одной смс, следует нажать на кнопку "🔂 Запросить еще смс"
- 1.6  Если все верно и вы хотите закончить работу с данным сервисом необходимо нажать кнопку "✅ Завершить заказ", либо активация успешно завершается автоматически по истечении времени (15 минут)
- 1.7  Максимальное время ожидания поступления смс составляет 15 минут, после чего выделение номера завершается.

2. Стоимость активаций списывается согласно прейскуранту (Отображается до покупки номера).
- 2.1 Деньги списываются с баланса по завершению операции (п.1.4,1.5 регламента).

3. Если номер выделен, но не использован (то есть вы не увидели код из смс), вы можете в любой момент отменить операцию без какого-либо штрафа. В случае злоупотребления или перебирания номеров в поиске лучшего, будут применены санкции на усмотрение модератора.

4. При использовании данного бота вы даёте согласие на получение рекламных материалов от @AVTOREGBOT.

5. История операций с номерами хранится на сервере и не подлежит удалению.

6.  Категорически запрещенно использование данного сервиса @AVROTERGBOT в любых противоправных целях.
- 6.1 Также запрещенно использовать данные номера с последующими целями, нарушающие Уголовный Кодекс Российской Федерации: обман, мошенничество и прочие (УК РФ 138, УК РФ 159, УК РФ 228, УК РФ 272, УК РФ 273, УК РФ 274)
- 6.2 Запрещено использование сервиса для осуществления платных подписок.

7. Мы не несем ответственности за созданные аккаунты, все действия, включая возможные блокировки, осуществляются исключительно на страх и риск конечного пользователя, который приобрел активацию

8. Возврат денежных средств предусмотрен только при подаче заявки на avtoregbot@bk.ru

9. Возврат денежных средств за ошибки пользователей - не предусмотрен

10. Использование ошибок или брешей в системе безопасности запрещено и квалифицируется по УК РФ ст.273
Нажимая на кнопку "Подтверждаю согласие", вы подтвердаете согласие с пользовательским соглашением."""


def main(userid):
	connection,q = connect()
	
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
	row = q.fetchone()
	q.execute(f'SELECT name FROM ugc_country WHERE id = "{row[3]}"')
	
	text = f'''❕ Привет тут ты можешь приобрести номера!
❕ Ваш баланс - {"%.2f" % float(row[2])} руб'''
	return text


def profile(message):
	connection,q = connect()
	
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{message.chat.id}"')
	row = q.fetchone()
	text = f'''🧾 Профиль

❕ Ваш id - {message.chat.id}
❕ Дата регистрации - {row[7]}
❕ Ваш логин - @{message.chat.username}

💰 Ваш баланс - {"%.2f" % float(row[2])} рублей
'''
	return text


def referals(userid):
	connection,q = connect()
	
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
	row = q.fetchone()
	q.execute(f'SELECT SUM(summa) FROM ugc_referals_buys WHERE ref = "{userid}" and ref_numb = "1"')
	first_ref_earn = q.fetchone()[0]
	q.execute(f'SELECT COUNT(id) FROM ugc_users WHERE ref1 = "{userid}"')
	one_refs = q.fetchone()
	# all_refs_count = f'{0 if all_refs[0] == None else int(all_refs[0]) +  0 if all_refs[1] == None else int(all_refs[1]) + 0 if all_refs[2] == None else int(all_refs[2]) }'
	text = f'''👥 Реферальная сеть

Ваша реферельная ссылка:
https://t.me/AVTOREGBOT?start={userid}

За все время вы заработали - {"%.2f" % float(row[6])} ₽
Вы пригласили - {one_refs[0]} людей

Если человек приглашенный по вашей реферальной ссылки пополнит баланс, то вы получите 30 % от суммы его депозита'

'''
	return text





def qiwi_pay(userid):
	connection,q = connect()
	
	q.execute(f'SELECT * FROM ugc_settings')
	row = q.fetchone()
	text = f'''Пополнение QIWI:
➖➖➖➖➖➖➖➖
👉 Номер  <code>{config.qiwi_number}</code>
👉 Коментарий  <code>{userid}</code>
➖➖➖➖➖➖➖➖

⚠️ Пополнение без комментария = деньги мне в карман так что сверяйте все чтобы было

⏳ После перевода средств дождитесь оповещения об успешной оплате.'''
	return text

def btc_pay(userid):
	text = f'''🏵 Вы выбрали пополнение баланса через чек BTC Banker. Следуйте указаниям:

Что бы пополнить баланс бота отправьте в личные сообщение бота (в этот же чат) <b>рублевый</b> BTC <b>чек</b> на желанную сумму.
Наша система <b>автоматически активирует чек</b> и пополнит Ваш баланс на сумму Вашего чека в течении <b>± минуты.</b>

‼️ Важно! Наша система принимает <b>только</b> чеки, <b>созданные в рублях!</b>
При возникновении ошибок обратитесь к менеджеру бота нажав в главном меню на кнопку «🔍Связь и правила»'''
	return text


def rent_text(userid, rentid):
	connection,q = connect()
	
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
	row = q.fetchone()
	q.execute(f'SELECT * FROM ugc_country WHERE id = "{row[3]}"') 
	country = q.fetchone()[2]
	q.execute(f'SELECT * FROM ugc_rent_list WHERE rentid = "{rentid}"')
	rent = q.fetchone()
	text = f'''❕ Вы успешно арендовали номер

Сервис: <code>{rent[2]}</code>
Номер телефона: <code>{rent[4]}</code>
Срок завершения аренды номера: <code>{rent[8]}</code>
'''
	return text

def rent_text_activ(userid, rentid):
	connection,q = connect()
	
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
	row = q.fetchone()
	q.execute(f'SELECT * FROM ugc_country WHERE id = "{row[3]}"') 
	country = q.fetchone()[2]
	q.execute(f'SELECT * FROM ugc_rent_list WHERE rentid = "{rentid}"')
	rent = q.fetchone()
	answer = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getRentStatus&id={rentid}').json()
	if answer['status'] == 'success':
		text = f'''Сервис: <code>{rent[2]}</code>
Номер телефона: <code>{rent[4]}</code>
Срок завершения аренды номера: <code>{rent[8]}</code>

📩 Сообщения:'''
		for i in answer['values']:
			print(i)
			text = f"{text}\nСмс: <code>{answer['values'][str(i)]['text']}</code>\nДата: {answer['values'][str(i)]['date']}\n"
	elif answer['status'] == 'error' and answer['message'] == 'STATUS_WAIT_CODE':
		text = f'''Сервис: <code>{rent[2]}</code>
Номер телефона: <code>{rent[4]}</code>
Срок завершения аренды номера: <code>{rent[8]}</code>

📩 Сообщения:'''

	elif answer['status'] == 'finish':
		text = f'''<b>НОМЕР ЗАВЕРШИЛ РАБОТУ</b>
Сервис: <code>{rent[2]}</code>
Номер телефона: <code>{rent[4]}</code>
Срок завершения аренды номера: <code>{rent[8]}</code>

📩 Сообщения:'''
		for i in answer['values']:
			print(i)
			text = f"{text}\nСмс: <code>{answer['values'][str(i)]['text']}</code>\nДата: {answer['values'][str(i)]['date']}\n"
		q.execute(f"""update ugc_rent_list set activ = '0' where rentid = '{rentid}' """)
		connection.commit()
	else:
		q.execute(f"""update ugc_rent_list set activ = '0' where rentid = '{rentid}' """)
		connection.commit()
		text = 'Номер завершил работу'

	return text


def admin_stata():
	connection,q = connect()
	
	now = datetime.datetime.now()
	time = now.strftime("%Y-%m-%d")
	time_two = now.strftime("%Y-%m-%d %H:")

	count_users = q.execute(f'SELECT COUNT(userid) FROM ugc_users').fetchone()[0]
	count_users_24 = q.execute(f'SELECT COUNT(userid) FROM ugc_users where date_reg LIKE "{time}%"').fetchone()[0]
	count_users_1 = q.execute(f'SELECT COUNT(userid) FROM ugc_users where date_reg LIKE "{time_two}%"').fetchone()[0]
	statistika_qiwi_24 = q.execute(f'SELECT SUM(summa) FROM ugc_pays where date_pay LIKE  "{time}%"').fetchone()[0]
	statistika_btc_24 = q.execute(f'SELECT SUM(summa) FROM ugc_pays_btc where date_pay LIKE "{time}%"').fetchone()[0]
	statistika_qiwi = q.execute(f'SELECT SUM(summa) FROM ugc_pays').fetchone()[0]
	statistika_btc = q.execute(f'SELECT SUM(summa) FROM ugc_pays_btc').fetchone()[0]

	text = f'''<b>❕ Информаци о пользователях:</b>

❕ За все время - <b>{count_users}</b>
❕ За день - <b>{count_users_24}</b>
❕ За час - <b>{count_users_1}</b>

<b>❕ Пополнений за 24 часа</b>
❕ QIWI: <b>{statistika_qiwi_24} ₽</b>
❕ BANKER: <b>{statistika_btc_24} ₽</b>

<b>⚠️ Ниже приведены данные за все время</b>
❕ Пополнения QIWI: <b>{statistika_qiwi} ₽</b>
❕ Пополнения BANKER: <b>{statistika_btc} ₽</b>
	'''
	return text


def country_list(service, tt,userid):
	try:
		connection,q = connect()
		
		if tt == '1':
			spisok = []
			q.execute(f'SELECT balance FROM ugc_users where userid = "{userid}"')
			balance = q.fetchone()[0]
			text_send = f'❕ Ваш баланс - {balance} руб\n❕ В наличии:\n➖➖➖➖➖➖➖➖\n'
			q.execute(f'SELECT * FROM ugc_service_all where code = "{service}" and spisok = "1"')
			row_site = q.fetchone()
			if row_site[6] == 'smshub':
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
								q.execute(f'SELECT name FROM ugc_country where idd = "{amm}"')
								row = q.fetchone()[0]
								q.execute(f'SELECT price FROM ugc_service_all where code = "{service}" and country = "{i[0]}" and price != "0"')
								# q.execute(f'SELECT price FROM ugc_service_all where code = "{service}" and country = "{i[0]}"')
								row_price = q.fetchone()
								if row_price != None:
									spisok.append(row_price)
									text_send = f'{text_send}{row} | {price} | {float(row_price[0])} ₽\n'
								else:
									continue
								break
					except:
						continue
			else:
				response = requests.get(url=f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.token_sms_activate}&action=getPrices&service={service}').json()
				q.execute(f'SELECT * FROM ugc_country')
				row_sitee = q.fetchall()
				for i in row_sitee:
					amm = i[2]
					try:
						answer = response[str(amm)][str(service)]
						if int(answer['count']) > 0:
							text = response[str(amm)][str(service)]['count']
							price = response[str(amm)][str(service)]['cost']
							q.execute(f'SELECT name FROM ugc_country where idd = "{amm}"')
							row = q.fetchone()[0]
							q.execute(f'SELECT price FROM ugc_service_all where code = "{service}" and country = "{i[0]}" and price != "0"')
							row_price = q.fetchone()[0]
							if row_price != None:
								spisok.append(row_price)
								text_send = f'{text_send}{row} | {text} | {float(row_price)} ₽\n'
							else:
								pass
					except:
						continue

			if len(spisok) >= 1:
				return text_send
			else:
				return 'На данный момент номеров нет, ожидайте пополнения!'
	except:
		pass


