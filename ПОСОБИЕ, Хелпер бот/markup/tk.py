import telebot
from telebot import types

tk_btn = [
	'TK 1.0',
	'TK 2.0',
	'🔙 Назад',

]

def tk_markup():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(
		tk_btn[0], 
		tk_btn[1], 
		tk_btn[2])

	return markup


tk1_btn = [
	'🚛 СДЭК: оплата ссылкoй',
	'📦 СДЭК 1.0',
	'🚚 Boxberry: оплата ссылкoй',
	'🚘 Boxberry 1.0',
	'🚖 Яндекс 1.0',
	'🌀 Яндекс 1.0 — 900',
	'🔙 Назад',

]

def tk1_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(tk1_btn[0], tk1_btn[1], 
		tk1_btn[2], tk1_btn[3], tk1_btn[4],
		tk1_btn[5], tk1_btn[6])

	return markup

tk2_btn = [
	'🛺 СДЭК 2.0',
	'🍕СДЭК 2.0:списание/баланс',
	'🔋 СДЭК 2.0:возврат',
	'🔕 СДЭК 2.0:нет уведомления',
	'🚗 Boxberry 2.0',
	'💌 Boxberry 2.0:запрос почты',
	'🚎 Почта РФ 2.0',
	'📧 Почта РФ 2.0:запрос Email',
	'🚐 Dostavista 2.0',
	'🚌 DHL 2.0',
	'↩️ DHL 2.0:возврат',
	'🚕 Яндекс 2.0',
	'🛍 Яндекс:списание/баланс',
	'🚙 ПЭК 2.0',
	'🔙 Назад',

]

def tk2_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(tk2_btn[0], tk2_btn[1],)
	markup.add(tk2_btn[2], tk2_btn[3], tk2_btn[4])
	markup.add(tk2_btn[5], tk2_btn[6])
	markup.add(tk2_btn[7], tk2_btn[8], tk2_btn[9])
	markup.add(tk2_btn[10], tk2_btn[11], tk2_btn[12])
	markup.add(tk2_btn[13], tk2_btn[14])

	return markup