from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button2 = InlineKeyboardButton(text="🎲 Игры", callback_data="button2")
button4 = InlineKeyboardButton(text="💥 Развлекательное", callback_data="button4")
button1 = InlineKeyboardButton(text="💡 Основные", callback_data="button1")
button6 = InlineKeyboardButton(text="🏰 Кланы", callback_data="button6")
kk = InlineKeyboardMarkup()
kk.row(button1, button4)
kk.row(button2)
kk.row(button6)




button10 = InlineKeyboardButton(text="Добавить бота 😄", url="https://t.me/quadroamineskinBot?startgroup=true")
nk2 = InlineKeyboardMarkup().add(button10)


kit_b1 = InlineKeyboardButton(text="  💚ВИП  ", callback_data="kit_b1")
kit_b2 = InlineKeyboardButton(text="  💙ЛЕГЕНДА  ", callback_data="kit_b2")
kit_b3 = InlineKeyboardButton(text="  💜СПОНСОР  ", callback_data="kit_b3")
kit_b4 = InlineKeyboardButton(text="  🖤ВЛАСТЕЛИН  ", callback_data="kit_b4")
kit_kb = InlineKeyboardMarkup()
kit_kb = (kit_b1, kit_b2)
kit_kb = (kit_b3, kit_b4)

don1 = InlineKeyboardButton(text="   📝Привилегии   ", callback_data="don1")
don2 = InlineKeyboardButton(text="   🆘Администрация   ", callback_data="don2")
don = InlineKeyboardMarkup().add(don1, don2)

game1 = InlineKeyboardButton(text="🕹️Играть", callback_data="game1")
gm = InlineKeyboardMarkup().add(game1)




