import telebot
from telebot import types


main_btn = [
	'🔗 Сократить ссылку',
	'🔎 Деанон',
	'♻️ Генератор',
	'ℹ️ Пробив',
	'🖼 Скриншот сайта',
	'⛩ Cкриншоты',
	'🧾 Диалоги',
	'📃 Мануалы',
	'🖥 Профиль',
	'📆 Информация',
]

screenshot_btn = [
	'🚙 Авито',
	'🚐 Юла',
	'🚚 ТК',
	'🏢 Недвижка',
	'📦 OLX',
	'🇧🇾 Куфар',
	'📱WhatsApp',
	'🛍 Яндекс Объявления',
	'🌀 BlaBlaCar',
	'🔙 Назад',
]

deanon_btn = [
	'🆔 Телеграм ID',
	'ℹ️ Пробив IP',
	'🔙 Назад',
]

dialogue_btn = [
	'👋 Приветствие',
	'🤏Вопросы о товаре',
	'💨Сказать о доставке',
	'✍️Другие вопросы',
	'🔙 Назад',

]

def main_menu():
	markup = types.ReplyKeyboardMarkup(row_width=3)
	markup.add(main_btn[0], main_btn[1], main_btn[2])
	markup.add(main_btn[3], main_btn[4])
	markup.add(main_btn[5], main_btn[6], main_btn[7])
	markup.add(main_btn[8], main_btn[9])

	return markup

def sreen_menu():
	markup = types.ReplyKeyboardMarkup(row_width=3)
	markup.add(screenshot_btn[0], screenshot_btn[1], screenshot_btn[2])
	markup.add(screenshot_btn[3], screenshot_btn[4])
	markup.add(screenshot_btn[5], screenshot_btn[6], screenshot_btn[7])
	markup.add(screenshot_btn[8], screenshot_btn[9])

	return markup

def deanon_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(deanon_btn[0], deanon_btn[1], deanon_btn[2])

	return markup

def dialog_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(dialogue_btn[0], dialogue_btn[1])
	markup.add(dialogue_btn[2], dialogue_btn[3], dialogue_btn[4])

	return markup


admin_sending_btn = [
    '✅ Начать', # 0
    '❌ Отменить' # 2
]

admin_sending = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
admin_sending.add(
    admin_sending_btn[0],
    admin_sending_btn[1],
)

def email_sending():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add( 
        types.InlineKeyboardButton(text='✔️ Рассылка(только текст)', callback_data='email_sending_text'), 
        types.InlineKeyboardButton(text='✔️ Рассылка(текст + фото)', callback_data='email_sending_photo'),
    )

    return markup


def admin_menu():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
		types.InlineKeyboardButton(text='Рассылка', callback_data='email_sending'),
    	types.InlineKeyboardButton(text='Информация', callback_data='admin_info'))

	return markup


















def profile_menu():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='Cтатистика', callback_data='my_stats'))

	return markup

def back_profile():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_prof'))

	return markup

def info():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='Админ', url='https://t.me/lanru7'))
	
	return markup

def generator():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='🔐 Генератор паролей', callback_data='gen_pass'),
    	types.InlineKeyboardButton(text='🧰 Генератор ников', callback_data='gen_nick'),
    	types.InlineKeyboardButton(text='🌐 Генератор прокси', callback_data='gen_proxy'),
	)
	return markup

def generator_pas():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='Легкий', callback_data='easy_pas'),
    	types.InlineKeyboardButton(text='Средний', callback_data='average_pas'),
    	types.InlineKeyboardButton(text='Cложный', callback_data='difficult_pas'),
	)
	return markup

def close():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='Закрыть', callback_data='to_close'))

	return markup


def manual():
	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(
    	types.InlineKeyboardButton(text='📕 Мануал по пополнению', url='https://telegra.ph/Manual-po-popolneniyu-10-03'),
    	types.InlineKeyboardButton(text='📗 Чем 2.0 лучше чем 1.0', url='https://telegra.ph/CHem-20-luchshe-chem-10-10-03'),
    	types.InlineKeyboardButton(text='📘 Частая ошибка новичков.', url='https://telegra.ph/CHastaya-oshibka-novichkov-10-03'),
    	types.InlineKeyboardButton(text='📙 Полезный совет', url='https://telegra.ph/Poleznyj-sovet-10-03'),
    	types.InlineKeyboardButton(text='📚 Мануал по эффективному Ворку', url='https://telegra.ph/Manual-po-ehffektivnomu-Vorku-10-03'),
	)
	return markup


bbk_btn = [
	'📃 Как проходит поездка',
	'💳 Оплата онлайн',
	'💰 Возврат',
	'🔙 Назад',

]

def bbk_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(bbk_btn[0])
	markup.add(bbk_btn[1], bbk_btn[2], bbk_btn[3])

	return markup


yandex_btn = [
	'📃 Как проходит получение денег',
	'🔗 Передать ссылку продавцу',
	'🔄 Оформление заказа',
	'📝 Запрос почты',
	'⛔️ Блокирует браузер',
	'🔙 Назад',

]

def yandex_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(yandex_btn[0])
	markup.add(yandex_btn[1], yandex_btn[2], 
		yandex_btn[3], yandex_btn[4], yandex_btn[5])

	return markup


wats_btn = [
	'🎤 Проблема с микрофоном',
	'📷 Проблема с камерой',
	'🔙 Назад',

]

def wats_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(wats_btn[0], wats_btn[1], wats_btn[2])

	return markup


kufar_btn = [
	'🚍 Куфар 2.0',
	'💳 2.0 — списание/баланс',
	'🔙 Назад',

]

def kufar_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(kufar_btn[0], kufar_btn[1], kufar_btn[2])

	return markup


realty_btn = [
	'🏬 Авито Недвижимость 2.0',
	'🏢 Циан 2.0',
	'↩️ Циан 2.0 возврат(ТП)',
	'↩️ Циан 2.0 возврат(ссылку)',
	'💸 Циан 2.0 списание/баланс',
	'🔙 Назад',

]

def realty_menu():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	markup.add(realty_btn[0])
	markup.add(realty_btn[1], realty_btn[2])
	markup.add(realty_btn[3], realty_btn[4], realty_btn[5])

	return markup
