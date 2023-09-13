import telebot
from telebot import types

olx_btn = [
	'🇺🇦 OLX UA',
	'🇰🇿 OLX KZ',
	'🇵🇱 OLX PL',
	'🇹🇩 OLX RO',
	'🇵🇹 OLX PO',
	'🇧🇬 OLX BU',
	'🔙 Назад',

]

def olx_markup():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(olx_btn[0], olx_btn[1], olx_btn[2],
		olx_btn[3], olx_btn[4], olx_btn[5],
		olx_btn[6])

	return markup


olx_ua_btn = [
	'🛍 2.0 Как работает доставка',
	'📦 1.0 Как работает доставка',
	'📪 Запрос почты',
	'💰Списание/баланс',
	'🌐 Получить по ссылке',
	'⬅️ Возврат',
	'🔙 Назад',

]

def olz_ua_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(olx_ua_btn[0], olx_ua_btn[1], 
		olx_ua_btn[2], olx_ua_btn[3], olx_ua_btn[4],
		olx_ua_btn[5], olx_ua_btn[6])

	return markup

olx_kz_btn = [
	'🇷🇼 OLX KZ 2.0 — как происходит получение денег',
	'🔙 Назад',

]

def olz_kz_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	markup.add(olx_kz_btn[0], olx_kz_btn[1])

	return markup


olx_ro_btn = [
	'📮 Запрос почты',
	'🎁 Товар оплачен',
	'⛔️ Лимит на карте',
	'🚨 Требуется подтверждение в приложении банка',
	'🔙 Назад',

]

def olz_ro_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(olx_ro_btn[0], olx_ro_btn[1],olx_ro_btn[2], )
	markup.add(olx_ro_btn[3])
	markup.add(olx_ro_btn[4],)

	return markup


olx_po_btn = [
	'📫 Запрос почты',
	'💸 Лимит на карте',
	'✉️ Push-уведомление',
	'🔙 Назад',

]

def olz_po_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(olx_po_btn[0], olx_po_btn[1], olx_po_btn[2])
	markup.add(olx_po_btn[3])

	return markup

olx_bu_btn = [
	'📬 Запрос почты',
	'📝 Как работает доставка',
	'🔙 Назад',

]

def olz_po_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(olx_bu_btn[0], olx_bu_btn[1])
	markup.add(olx_bu_btn[2])

	return markup


olx_pl_btn = [
	'🗒 Запрос почты',
	'💸 Нет баланса',
	'📰 Как работает доставка',
	'💳 Лимит на карте',
	'🔗 Сообщить ссылку продавцу',
	'🛍 Товар оплачен',
	'✅ Требуется подтверждение в приложении банка',
	'🔙 Назад',

]

def olz_pl_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	markup.add(olx_pl_btn[0], olx_pl_btn[1], olx_pl_btn[2])
	markup.add(olx_pl_btn[3], olx_pl_btn[4], olx_pl_btn[5])
	markup.add(olx_pl_btn[6])
	markup.add(olx_pl_btn[7])

	return markup