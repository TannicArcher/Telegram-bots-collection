from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, executor, types
from config import config


API_TOKEN = config('USER_BOT') # bot token

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✨ Получить ✨", web_app=WebAppInfo(url=config('user_link')))] # сюда ссылку
    ],
    resize_keyboard=True
)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await bot.send_message(message.chat.id,
                           config('USER_MSG'),
                           reply_markup=keyboard)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
