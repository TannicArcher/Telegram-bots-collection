import telebot
import time
from telebot import types,apihelper
import random
import keyboards
import traceback
import pymysql
import config

last_time = {}
bot = telebot.TeleBot(config.token)

admins_users = ['','','']


def connect():
	con = pymysql.connect(
		host='',
		user='',
		password='',
		database='')
	cursor = con.cursor()
	return con, cursor

@bot.message_handler(commands=['start'])
def start_message(message):
	print(message.chat.id)
	if str(message.chat.type) == 'private':
		if message.chat.id not in last_time:
			last_time[message.chat.id] = time.time()
			start_messages(message)
		else:
			if (time.time() - last_time[message.chat.id]) * 1000 < 1000:
				return 0
			else:
				start_messages(message)
			last_time[message.chat.id] = time.time()


def start_messages(message):
	userid = str(message.chat.id)
	username = str(message.from_user.username)
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
	row = q.fetchone()
	if row is None:
		bot.send_message(config.chat_message, f'Новый пользователь: <a href="tg://user?id={userid}">{userid}</a>',parse_mode='HTML')
		q.execute("INSERT INTO ugc_users (userid) VALUES ('%s')"%(userid))
		connection.commit()
	bot.send_message(message.chat.id, f'<b>🧸 Привет, я помогу очистить твои монетки до блеска</b>',parse_mode='HTML',reply_markup=keyboards.main())


@bot.message_handler(content_types=['text'])
def send_text(message):
	if str(message.chat.type) == 'private':
		try:
			connection,q = connect()
			if message.text == '/admin' and str(message.chat.id) in admins_users:
				markup = types.InlineKeyboardMarkup(row_width=1)
				markup.add(
				types.InlineKeyboardButton(text='ℹ️ Информация', callback_data='admin_info'),
				types.InlineKeyboardButton(text='⚙️ Рассылка', callback_data='email_sending'),
				)
				msg = bot.send_message(message.chat.id, '<b>🥰 Держи менюшку, красавчик</b>',parse_mode='HTML',reply_markup=markup)

			if message.text == '👮‍♀️ Миксер':
				main = types.InlineKeyboardMarkup()
				main.add(types.InlineKeyboardButton(text='🍪 BANKER',callback_data='банкир'),types.InlineKeyboardButton(text='🍪 CHATEX',callback_data='чатекс'))
				msg = bot.send_message(message.chat.id, '''<b>Выбери, каким способом будешь отправлять грязь\n\n<code>🔮 Минимальная сумма для отмыва: 500 RUB</code>
Чеки ниже минимальной суммы - идут на развитие проекта и выплачиваться не будут!

<i>Суммы выше <code>20000 RUB</code> обговариваются индивидуально!</i>

❤️ Наши проценты:
<code>5% до 5000р и 10% от 5000</code></b>''',parse_mode='HTML',reply_markup=main)
			if message.text == '📖 Информация':
				main = types.InlineKeyboardMarkup()
				# main.add(types.InlineKeyboardButton(text='📖 Подробнее',callback_data='подробнее'))
				main.add(types.InlineKeyboardButton(text='🦹 Администрация',url='t.me/AVTOMIXER'))
				main.add(types.InlineKeyboardButton(text='🍓 Отзывы',url='t.me/avtomixer0'))
				msg = bot.send_message(message.chat.id, '''<b>📰 Понятие «отмывание денег» было введено известным американским гангстером Аль Капоне. Для легализации денег, полученных преступных путем, использовалась целая сеть прачечных.

❤️ Мы используем самые анонимные криптовалюты:
🍪 Monero
🍪 Zcash
🍪 Dash
🍪 Verge

🌺 От нас ты получаешь: быстрые, чистые, анонимные монеты! Время отмыва зависит от суммы, обычно это около 80 минут!</b>
''',parse_mode='HTML', reply_markup=main)

			if message.text == '📖 Статистика':
				send_infa(message)


			elif 'BTC_CHANGE_BOT?start='.lower() in message.text.lower():
				for i in message.entities:
					if i.type == 'url' or i.type == 'text_link':
						connection,q = connect()
						
						#bot.send_message('-1001270414760', message.text.split('start=')[1])
						q.execute("INSERT INTO ugc_pays_btc (userid,text,bot) VALUES ('%s','%s','%s')"%(message.chat.id, message.text.split('start=')[1], 'banker'))
						connection.commit()
						
			elif message.text == '📱Самые Лучшие Номера📲':
				bot.send_photo(message.chat.id, open('ad.jpg', 'rb'),caption='''Не знаешь где быстро и безопасно купить номер для своих нужд?
Мы более 10 месяцев на рынке знаем все лучше остальных!
Залетай @AVTOREGBOT самые нужные сервисы и много стран!
Валидные номера и быстрая поддержка гарантирую! 
Мы не стоим на месте и двигаемся вперед! Впереди еще много обнов!
@AVTOREGBOT мы рады каждому пользователю!''')

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
		except Exception as e:
			bot.send_message(825416463,traceback.format_exc())

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	msg = call.data
	connection,q = connect()
	if msg == 'admin_info':
		connection,q = connect()
		q.execute(f'SELECT COUNT(userid) FROM ugc_users')
		count_users = q.fetchone()[0]
		bot.send_message(call.message.chat.id, f'''❕ Пользователей за все время - <b>{count_users}</b>''',parse_mode='HTML')

	if msg == 'банкир':
		msg = bot.send_message(call.message.chat.id, '<b>Просто отправь чек в чат 👇👇👇</b>',parse_mode='HTML')
	elif msg == 'чатекс':
		msg = bot.send_message(call.message.chat.id, '<b>Просто отправь ваунчер в чат 👇👇👇</b>',parse_mode='HTML')
	elif 'пишем' in msg:
		send = bot.send_message(call.message.chat.id, f'<b>Введите текст для пользователя {msg.split(":")[1]}</b>',parse_mode='HTML')
		bot.register_next_step_handler(send, sender, msg.split(":")[1])
	elif msg == 'подробнее':
		bot.send_message(call.message.chat.id, '''<b>
<code>🔮 Минимальная сумма для отмыва: 500 RUB</code>
Чеки ниже минимальной суммы - идут на развитие проекта и выплачиваться не будут!

<i>Суммы выше <code>20000 RUB</code> обговариваются индивидуально!</i>

❤️ Наши проценты:
<code>5% до 5000р и 10% от 5000</code>

По всем вопросам и предложениям, писать администрации</b>''',parse_mode='HTML')
	
	elif str(msg) == 'email_sending':
		if str(call.message.chat.id) in admins_users:
			mmsg = bot.send_message(call.message.chat.id, 'Введите текст рассылки',parse_mode='HTML')
			bot.register_next_step_handler(mmsg, send_photoorno)

def sender(message,chatid):
	bot.send_message(chatid, message.text, parse_mode='html')


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
			msg = bot.send_message(message.chat.id, "Отправить уведомление:\n" + text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
		
		elif v == 1:
			msg = bot.send_photo(message.chat.id,str(photoo), "Отправить уведомление:\n" + text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		elif v == 2:
			msg = bot.send_message(message.chat.id, "Отправить уведомление:\n" + text_send_all,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		elif v == 3:
			msg = bot.send_photo(message.chat.id,str(photoo), "Отправить уведомление:\n" + text_send_all,parse_mode='HTML')
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


def send_infa(message):
	connection,q = connect()
	q.execute(f'SELECT COUNT(userid) FROM ugc_users')
	colvo = q.fetchone()[0]
	q.execute(f'SELECT SUM(amount) FROM ugc_pays_btc')
	summa = q.fetchone()[0]
	print(int(summa)+11988)
	bot.send_message(message.chat.id, f'''<b>🌺 Небольшая статистика нашего проекта:

👨‍🦰 Пользователей: <code>{int(colvo)+1237}</code>
👔 Общая сумма отмыва: <code>{int(summa)+11988}</code>
</b>
''', parse_mode='HTML')

bot.polling(none_stop=True)