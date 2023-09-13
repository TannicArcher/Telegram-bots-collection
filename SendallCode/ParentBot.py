from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


#SCRIPT BY @NOTIDIOS #SCRIPT BY @NOTIDIOS #SCRIPT BY @NOTIDIOS #SCRIPT BY @NOTIDIOS #SCRIPT BY @NOTIDIOS #SCRIPT BY @NOTIDIOS #SCRIPT BY @NOTIDIOS


TOKEN = '5962946342:AAGhG1xkrfwdfJSiO9PPurV-AyISEO2vOfg'

Bot = Bot(token=TOKEN)
dp = Dispatcher(Bot)
db = Database('database.db')

online = 'Бот вышел в онлайн'

async def on_startup(_):
    print(online)

@dp.message_handler(commands='start')
async def welcome(message : types.Message):
    await Bot.send_message(message.from_user.id, "<b> Добро пожаловать ! \n\nЭто скрипт написанный за 5 минут от @Notidiots\nпиши /sendall свой текст</b>", parse_mode='HTML')

@dp.message_handler(commands=['sendall'])
async def get_all(message: types.Message):
    if message.chat.type == 'private':
        if (message.from_user.id == Ваш айди в телеграмме):
            text = message.text[9:]
            users = db.get_user()
            for row in users:
                try:
                    await Bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    pass
    if (message.from_user.id == Ваш айди в телеграмме):
        await Bot.send_message(message.from_user.id, "<b>Успешная рассылка !</b>", parse_mode='HTML')
    else:
        await Bot.send_message(message.from_user.id, "Ты не админ")



executor.start_polling(dp, skip_updates=True)