import telebot
from telebot import types

youla_btn = [
	'Юла 1.0',
	'Юла 2.0',
	'Юла 3.0',
	'Юла Блок браузера',
	'🔙 Назад',

]

def youla_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(
		youla_btn[0], 
		youla_btn[1], 
		youla_btn[2],
		youla_btn[3],
		youla_btn[4],)

	return markup

youla1_btn = [
	'📨 Запрос почты',
	'🧷 Оплата по ссылке',
	'📝 900',
	'🔙 Назад',

]

def youla1_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(youla1_btn[0]) 
	markup.add(youla1_btn[1], youla1_btn[2], youla1_btn[3])

	return markup


youla2_btn = [
	'📅 Заказ оформлен (SMS)',
	'🔗 Подозрение в домене',
	'📖 Запрос почты',
	'📍 Списание/баланс',
	'📌 CVC код',
	'📋 Нет уведомления',
	'✅ Сообщить ссылку',
	'🔙 Назад',
	'🔚 Далее',

]

def youla2_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(youla2_btn[0], youla2_btn[1]) 
	markup.add(youla2_btn[2], youla2_btn[3], youla2_btn[4])
	markup.add(youla2_btn[5], youla2_btn[6])
	markup.add(youla2_btn[7], youla2_btn[8])

	return markup

youla3_btn = [
	'🔗 Получить по ссылке',
	'↩️ Возврат',
	'⭕️ 900',
	'🔒 Зачем нужно резервирование',
	'📛 Возврат будет долгим',
	'📕 Как работает доставка',
	'📗 Как работает доставка2',
	'🔙 Назад',
]

def youla3_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(youla3_btn[0], youla3_btn[1]) 
	markup.add(youla3_btn[2], youla3_btn[3], youla3_btn[4])
	markup.add(youla3_btn[5], youla3_btn[6])
	markup.add(youla3_btn[7])

	return markup
