from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_button = ReplyKeyboardMarkup(resize_keyboard=True,
                                       keyboard=[
                                           [
                                               KeyboardButton("🏡 Меню")
                                           ]
                                       ]
                                       )
