from casino_config import bot, types, in_deposit, user_status_pay, status_bot
from casino_config import user_invite_code, user_update_code, token, phone, enter_promo, bill_create, phone
from casino_config import nvuti, dice, coinflip, crash, crash_end, clear_stats, deposit, enter_receive
import casino_config, database, keyboard
import threading, time, configparser

@bot.message_handler(commands=['start'])  
def start_command(message):
	try:
		chat_id = message.chat.id
		code = message.text.split()

		if (not database.user_exists_casino(chat_id)):
			if (len(code) == 2):
				exists = database.worker_exists_code(code[1])

				if (exists is not False):
					username = message.from_user.username

					database.user_add_casino(chat_id, username, code[1])
					bot.send_message(chat_id, f"🙋🏻‍♀️ Добро пожаловать, *{message.from_user.first_name}*\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
						parse_mode="Markdown", reply_markup = keyboard.casino_keyboard())

					casino_config.notification_thread_ref(code[1], message.from_user.first_name, username)
				else:	
					message = bot.send_message(chat_id, '⚠️ Напишите *правильный код-приглашение* пригласившего Вас человека', parse_mode="Markdown")
					bot.register_next_step_handler(message, user_invite_code)
			else:
				message = bot.send_message(chat_id, '💁🏻‍♀️ Для начала работы, *напишите код-приглашение* пригласившего Вас человека', parse_mode="Markdown")
				bot.register_next_step_handler(message, user_invite_code)
		else:
			if (database.user_invite_code(chat_id) == '0'):
				message = bot.send_message(chat_id, '💁🏻‍♀️ Для начала работы, *напишите код-приглашение* пригласившего Вас человека', parse_mode="Markdown")
				bot.register_next_step_handler(message, user_update_code)
			else:
				bot.send_message(chat_id, f"🙋🏻‍♀️ Добро пожаловать, *{message.from_user.first_name}*\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
					parse_mode="Markdown", reply_markup = keyboard.casino_keyboard())
	except:
		bot.send_message(chat_id, "⚠️ Ошибка при *регистрации* пользователя. Повторите попытку снова написав /start", parse_mode="Markdown")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	chat_id = message.chat.id

	config = configparser.ConfigParser()
	config.read("default.ini")
	status = config['Telegram']['messages']

	try:
		if (status != '0'):
			if (message.text == "Личный кабинет"):

				balance 	= casino_config.repl_percent(database.user_balance(chat_id))
				win 		= database.user_win(chat_id)
				lose		= database.user_lose(chat_id)
				receive 	= database.user_receives(chat_id)
				payments 	= database.user_count_payments(chat_id)

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
				inline_1 = types.InlineKeyboardButton(text = "Пополнить", callback_data = 'DEPOSIT')
				inline_2 = types.InlineKeyboardButton(text = "Вывести", callback_data = 'RECEIVE')
				inline_3 = types.InlineKeyboardButton(text = "Промокод", callback_data = 'PROMOCODE')
				inline_4 = types.InlineKeyboardButton(text = "Обнулить", callback_data = 'CLEAR')
				inline_keyboard.add(inline_1, inline_2, inline_3, inline_4)

				bot.send_message(chat_id, f'💸 Ваш *личный кабинет*\n\nБаланс: *{balance}* ₽\n\nИгр всего - *{win + lose}*\nИгр выиграно - *{win}*\nИгр проиграно - *{lose}*'
					+ f'\n\nЗаявок на вывод - *{receive}*\nПополнений - *{payments}*',
					parse_mode="Markdown", reply_markup=inline_keyboard)
			elif (message.text == "Тех. Поддержка"):
				bot.send_message(chat_id, f'💻 Техническая поддержка - @{str(casino_config.support)}')
			elif (message.text == "Играть"):
				database.user_update_username(chat_id, casino_config.repl(message.from_user.username))
				bot.send_message(chat_id, f'💁🏻‍♀️ Выберите *режим* игры', parse_mode="Markdown", reply_markup=keyboard.game_keyboard())
			elif (message.text == "Назад"):
				bot.send_message(chat_id, f'💁🏻‍♀️ Вы вернулись в *главное* меню', parse_mode="Markdown", reply_markup=keyboard.casino_keyboard())
			elif (message.text == "Random Number"):
				balance 	= casino_config.repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)
			elif (message.text == "Dice"):
				balance 	= casino_config.repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
			elif (message.text == "Орел & Решка"):
				balance 	= casino_config.repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, coinflip)
			elif (message.text == "Назaд"):
				bot.send_message(chat_id, f'💁🏻‍♀️ Вы вернулись в *главное* меню', token, phone, parse_mode="Markdown", reply_markup=keyboard.casino_keyboard())
			elif (message.text == 'Crash'):
				balance 	= casino_config.repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, crash)
			elif (message.text == "Остановить график"):
				crash_end(message)
			elif (message.text == "Помoшь"):
				bot.send_message(chat_id, f'💻 Техническая поддержка - @{str(casino_config.helps)}')
			elif (message.text == 'Завершить игру'):
				bot.send_message(chat_id, f'💁🏻‍♀️ Вы вернулись в *список* игр', parse_mode="Markdown", reply_markup=keyboard.game_keyboard())
		else:
			bot.send_message(chat_id, '💁🏻‍♀️ Бот на *технических* работах', parse_mode="Markdown")
	except:
		pass

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	chat_id = call.message.chat.id
	
	try:
		if (call.data == 'PROMOCODE'):
			message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *промокод*', parse_mode="Markdown")
			bot.register_next_step_handler(message, enter_promo)
		elif (call.data == "CLEAR"):
			clear_stats(call)
		elif (call.data == "DEPOSIT"):
			message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* пополнения (от 250 ₽ до 5000 ₽)', parse_mode="Markdown")
			bot.register_next_step_handler(message, deposit)
		elif (call.data == "STATUS"):
			Thread = threading.Thread(target = user_status_pay, args = (call,))
			Thread.start()
		elif (call.data == "RECEIVE"):
			message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *свой* QIWI кошелек\nВо избежании мошенничества вывод разрешён только на те QIWI, с которых поступало пополнение!', parse_mode="Markdown")
			bot.register_next_step_handler(message, enter_receive)
	except:
		pass
		
bot.polling(none_stop = True, interval = 0)			