import telebot
from telebot import types

avito_btn = [
	'Авито 1.0',
	'Авито 2.0',
	'Авито 3.0',
	'Блокирует браузер',
	'🔙 Назад',

]

def avito_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(
		avito_btn[0], 
		avito_btn[1], 
		avito_btn[2],
		avito_btn[3],
		avito_btn[4],)

	return markup

avito1_btn = [
	'📧 Запрос почты',
	'🔌 Оплата по ссылке',
	'📞 900',
	'🔙 Назад',

]

def avito1_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(avito1_btn[0]) 
	markup.add(avito1_btn[1], avito1_btn[2], avito1_btn[3])

	return markup


avito2_btn = [
	'♻️ Нужна почта/оформление заказа',
	'🛍 Заказ оформлен (SMS)',
	'🔑 Подозрение в домене',
	'✉️ Запрос почты',
	'💳 Списание/баланс',
	'🔐 CVC код',
	'🔕 Нет уведомления',
	'🔙 Назад',
	'Далее',

]

def avito2_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(avito2_btn[0], avito2_btn[1]) 
	markup.add(avito2_btn[2], avito2_btn[3], avito2_btn[4])
	markup.add(avito2_btn[5], avito2_btn[6])
	markup.add(avito2_btn[7], avito2_btn[8])

	return markup

avito3_btn = [
	'🔗 Получить по ссылке',
	'↩️ Возврат',
	'📱 900',
	'💷 получение денег',
	'🕥 Возврат будет долгим',
	'📋 Как работает доставка',
	'🗒 Как работает доставка2',
	'📨 Фейковый почтовый домен',
	'🔙 Назад',
]

def avito3_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(avito3_btn[0], avito3_btn[1]) 
	markup.add(avito3_btn[2], avito3_btn[3], avito3_btn[4])
	markup.add(avito3_btn[5], avito3_btn[6])
	markup.add(avito3_btn[7], avito3_btn[8])

	return markup
