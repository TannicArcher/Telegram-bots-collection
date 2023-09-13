import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, number, QIWI_SEC_TOKEN, sum, admin
import keyboard as k
import functions as fc
import text as tx
import sqlite3
from qiwipyapi import Wallet

#Бот слит в телеграм канале @END_SOFT
# Логи в консоль
logging.basicConfig(level=logging.INFO)
#Бот слит в телеграм канале @END_SOFT

# Инициализация
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#Бот слит в телеграм канале @END_SOFT

connection = sqlite3.connect('data.db')
q = connection.cursor()

#Бот слит в телеграм канале @END_SOFT

wallet_p2p = Wallet(number, p2p_sec_key=QIWI_SEC_TOKEN)

#Бот слит в телеграм канале @END_SOFT

@dp.message_handler(commands=['start', 'help']) # Начало работы
async def start(message: types.Message):
	q.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchall()
	if len(result) == 0:
			q.execute(f"INSERT INTO users (user_id, balance)"
						f"VALUES ('{message.chat.id}', '0')")
			connection.commit()
			await message.answer(tx.sogl, parse_mode='Markdown', reply_markup=k.accept)
	else:
		await message.answer(
		f'Привет, {message.from_user.mention}, кликай и зарабатывай! За каждый клик вам начисляется 10 копеек на баланс.',
		reply_markup=k.menu)

#Бот слит в телеграм канале @END_SOFT


@dp.message_handler(content_types=["text"]) # Реакция на текст#Бот слит в телеграм канале @END_SOFT

async def reaction(message: types.Message):
	chat_id = message.chat.id
	fc.first(chat_id=chat_id)
	if message.text == '👤 Баланс':
		bal = q.execute(f'SELECT balance FROM users WHERE user_id = "{message.chat.id}"').fetchone()
		connection.commit()
		await message.answer(f'Ваш баланс: {fc.toFixed(bal[0], 1)}₽')
	elif message.text == '💸 Клик':
		q.execute(f'UPDATE users SET balance = balance + 0.1 WHERE user_id IS "{message.chat.id}"')
		connection.commit()
		
		await message.answer('Вам начислено +0.1₽')
	elif message.text == '🎰 Вывод':
		payed = q.execute(f'SELECT payd FROM users WHERE user_id = "{message.chat.id}"').fetchone()
		connection.commit()
		if payed[0] == 0:
			await message.answer(tx.ver ,reply_markup=k.pay)#Бот слит в телеграм канале @END_SOFT

		else:
			bal = q.execute(f'SELECT balance FROM users WHERE user_id = "{message.chat.id}"').fetchone()
			connection.commit()
			await message.answer(f'Заявка на вывод успешно отправлена администраторам, с вами скоро свяжутся.', reply_markup=k.menu)
			await bot.send_message(admin, f'Новая заявка на вывод:\nID - {message.chat.id}\nЮзернейм - {message.from_user.mention}\n[Ссылка на пользователя]({message.from_user.url})\nБаланс - {fc.toFixed(bal[0], 1)}\nСвяжитесь с пользователем, чтобы отправить ему деньги.', parse_mode='Markdown')
			q.execute(f"UPDATE USERS SET payd = 0 WHERE user_id = {chat_id}")
			connection.commit()
	elif message.text == 'Оплатить':
		link = fc.pay(chat_id=chat_id)
		await message.answer(f'Ваш ID - {message.chat.id}\nК оплате - {sum}₽\n[Ссылка для оплаты]({link})', reply_markup=k.buy1, parse_mode='Markdown')
	elif message.text == '/admin':
		if str(chat_id) == str(admin):
			await message.answer('Добро пожаловать в админ панель:', reply_markup=k.apanel)
		else:
			await message.answer('Черт! Ты меня взломал🙃')
#Бот слит в телеграм канале @END_SOFT
@dp.callback_query_handler(lambda call: True) # Inline часть#Бот слит в телеграм канале @END_SOFT
async def cal(call):
	chat_id = call.message.chat.id
	if call.data == 'check':
		try:
			re = q.execute(f"SELECT bd FROM users WHERE user_id = {chat_id}").fetchone()
			status = wallet_p2p.invoice_status(bill_id=re[0])
			a = status['status']['value']
			if a == 'WAITING':
				await call.message.answer('Ошибка! Платёж не найден.', reply_markup=k.buy1)
			elif a == 'PAID':
				await call.message.answer('Оплата успешно найдена.\nТеперь вы можете вывести баланс.', reply_markup=k.menu)
				q.execute(f'UPDATE users SET payd = 1 WHERE user_id IS "{chat_id}"')
				q.execute(f'UPDATE users SET bd = 0 WHERE user_id IS "{chat_id}"')
				connection.commit()
			elif a == 'EXPIRED':
				await call.message.answer('Время жизни счета истекло. Счет не оплачен', reply_markup=k.buy1)
			elif a == 'REJECTED':
				await call.message.answer('Счет отклонен', reply_markup=k.buy1)
			elif a == 'UNPAID':
				await call.message.answer('Ошибка при проведении оплаты. Счет не оплачен', reply_markup=k.buy1)
		except Exception as err:
			await call.message.answer('Ошибка!')
	elif call.data == 'stats':
		re = q.execute(f'SELECT * FROM users').fetchall()
		kol = len(re)
		bal = q.execute(f"SELECT sum(balance) FROM users").fetchone()
		connection.commit()
		await call.message.answer(f'Всего пользователей: {kol}\nОбщий баланс всех пользователей: {fc.toFixed(bal[0], 1)}₽')
	elif call.data == 'back':
		await call.message.answer('Назад..', reply_markup=k.menu)
	elif call.data == 'accept':
		await call.message.answer(
		f'Привет, {call.from_user.mention}, кликай и зарабатывай! За каждый клик вам начисляется 10 копеек на баланс.',
		reply_markup=k.menu)
#Бот слит в телеграм канале @END_SOFT


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True) # Запуск
#Бот слит в телеграм канале @END_SOFT#Бот слит в телеграм канале @END_SOFT