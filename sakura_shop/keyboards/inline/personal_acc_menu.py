from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ======================== PERSONAL ACCOUNT MARKUP ========================
personal_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📥Пополнить баланс📥", callback_data="deposit")
        ],
        [
            InlineKeyboardButton(text="📖Все заказы", callback_data="my_orders"),
            InlineKeyboardButton(text="📖Статус заказа", callback_data="show_order_status")
        ],
        [
            InlineKeyboardButton(text="🔰Ввести промокод🔰", callback_data="promo")
        ],
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="back_to_main_menu")
        ]
    ]
)


# ======================== ORDERS MARKUP ========================
my_orders_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="personal_acc")
        ]
    ]
)
