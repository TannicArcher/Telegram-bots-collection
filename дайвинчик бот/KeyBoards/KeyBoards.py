from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

main_menu_KeyBoard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

main_menu_KeyBoard.add("Посмотреть все анкеты")
main_menu_KeyBoard.add("Посмотреть мои симпатии")
main_menu_KeyBoard.add("Моя анкета")

change_anket_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

change_anket_menu.add("Изменить фото")
change_anket_menu.add("Изменить описание")
change_anket_menu.add("Отмена")

show_ankets_KeyBoard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

show_ankets_KeyBoard.add("Следущая")
show_ankets_KeyBoard.add("Симпатия")
show_ankets_KeyBoard.add("Отмена")


admin_KeyBoard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

admin_KeyBoard.add("Hello")
admin_KeyBoard.add("Изменить данные для входа")
admin_KeyBoard.add("Отмена")

end_anekets_KeyBoard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
end_anekets_KeyBoard.add("Смотреть старые анкеты")
end_anekets_KeyBoard.add("Отмена")

next_anket = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
next_anket.add(InlineKeyboardMarkup(text="Следущая", callback_data="next"))
next_anket.add(InlineKeyboardMarkup(text="Нравиться", callback_data="like"))
