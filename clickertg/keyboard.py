from aiogram import Bot, Dispatcher, executor, types


#Бот слит в телеграм канале @END_SOFT
# Клавиатура
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
	types.KeyboardButton('👤 Баланс'),
	types.KeyboardButton('💸 Клик'),
	types.KeyboardButton('🎰 Вывод')
)#Бот слит в телеграм канале @END_SOFT

pay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pay.add(
	types.KeyboardButton('Оплатить')
)
#Бот слит в телеграм канале @END_SOFT
accept = types.InlineKeyboardMarkup(row_width=3)
accept.add(
    types.InlineKeyboardButton(text='✅ Принимаю', callback_data='accept')
)
#Бот слит в телеграм канале @END_SOFT
buy1 = types.InlineKeyboardMarkup(row_width=3)
buy1.add(
    types.InlineKeyboardButton(text='Проверить оплату', callback_data='check'),
    types.InlineKeyboardButton(text='Назад', callback_data='back')
    )
#Бот слит в телеграм канале @END_SOFT
apanel = types.InlineKeyboardMarkup(row_width=3)
apanel.add(
    types.InlineKeyboardButton(text='Статистика', callback_data='stats')
    )