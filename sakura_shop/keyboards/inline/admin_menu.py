from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import select_categories, select_items, select_product_subcategories, \
    select_smm_subcategories, select_product_items, select_product_subcategory, select_all_mails, select_mail

# ========================ADMIN MENU========================
admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📮Рассылка", callback_data="broadcast"),
            InlineKeyboardMarkup(text="⚙️Настройки", callback_data="edit_settings")
        ],
        [
            InlineKeyboardButton(text="📥Выдать баланс", callback_data="balance:add"),
            InlineKeyboardButton(text="📤Забрать баланс", callback_data="balance:remove")
        ],
        [
            InlineKeyboardButton(text="📌Добавить", callback_data="add"),
        ],
        [

            InlineKeyboardButton(text="📊Статистика", callback_data="admin_stat"),
            InlineKeyboardButton(text="🔎 Найти юзера", callback_data="get_user")
        ],
        [
            InlineKeyboardButton(text="✏️ Изменить", callback_data="edit_buttons"),
            InlineKeyboardButton(text="📨Поддержка", callback_data="help")
        ],
        [
            InlineKeyboardButton(text="🔙В главное меню", callback_data="back_to_main_menu")
        ]
    ]
)

# ======================== BROADCAST MARKUP ========================
broadcast_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌Скрыть", callback_data="delete_this_message")
        ]
    ]
)

edit_buttons_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📦Товары", callback_data="edit:product"),
            InlineKeyboardButton(text="📊 Накрутка ", callback_data="edit:smm")
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

# START BROADCAST
choose_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅Да", callback_data="yes")
        ],
        [
            InlineKeyboardButton(text="❌Отмена", callback_data="no")
        ]
    ]
)

# ======================== BACK TO ADMIN MENU BUTTON ========================
back_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

# ======================== TYPE OF BUTTONS TO DELETE MENU ========================
delete_button_type_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📌Категория", callback_data="del_button:category")
        ],
        [
            InlineKeyboardButton(text="📌Под-категория", callback_data="del_button:subcategory"),
        ],
        [
            InlineKeyboardButton(text="📌Услуга", callback_data="del_button:item")
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

button_type_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Накрутка ", callback_data="add_button:smm")
        ],
        [
            InlineKeyboardButton(text="📦 Товары", callback_data="add_button:product"),
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

product_type_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Текст", callback_data="product_type:text")
        ],
        [
            InlineKeyboardButton(text="Файл", callback_data="product_type:file"),
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)


# ======================== TYPE OF BUTTONS TO ADD MENU ========================
async def add_button_type_menu(button_type):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📌Категория", callback_data=f"button_type:category:{button_type}")
            ],
            [
                InlineKeyboardButton(text="📌Под-категория", callback_data=f"button_type:subcategory:{button_type}"),
            ],
            [
                InlineKeyboardButton(text="📌Услуга/товар", callback_data=f"button_type:item:{button_type}")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
            ]
        ]
    )
    return keyboard


# ======================== GET USER MARKUP ========================
get_user_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎊Изменить бонус", callback_data="edit_bonus")
        ],
        [
            InlineKeyboardButton(text="👤Список рефералов", callback_data="ref_list")
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

# ======================== GENERAL SETTINGS MARKUP ========================
admin_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔐 Настроить кошелёк", callback_data="choose_settings:wallet")
        ],
        [
            InlineKeyboardButton(text="🎁 Настроить канал", callback_data="choose_settings:gift")
        ],
        [
            InlineKeyboardButton(text="💾 Настроить логирование", callback_data="edit_log_channel")

        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
        ]
    ]
)

# ======================== WALLET SETTINGS MARKUP ========================
wallet_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔑 Ввести токен", callback_data="settings:token")
        ],
        [
            InlineKeyboardButton(text="📱 Ввести номер", callback_data="settings:num")
        ],
        [
            InlineKeyboardButton(text="🗝 Публичный ключ", callback_data="settings:p2p")

        ],
        [
            InlineKeyboardButton(text="🔐 Секретный ключ", callback_data="edit_qiwi_secret")
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="edit_settings")
        ]
    ]
)

# ======================== GIFT SETTINGS MARKUP ========================
gift_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔗 Изменить Ссылку  ", callback_data="edit_channel_url")
        ],
        [
            InlineKeyboardButton(text="🆔 Изменить ID", callback_data="edit_channel_id")
        ],
        [
            InlineKeyboardButton(text="⬅️Назад", callback_data="edit_settings")
        ]
    ]
)


# ======================== ALL CATEGORIES TO ADD/DELETE ========================
async def admin_all_categories(item_type):
    categories = await select_categories(category_type=item_type)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        keyboard.insert(InlineKeyboardButton(text=category[0], callback_data=f"adm_cat:{category[1]}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_admin"))
    return keyboard


# ======================== SUBCATEGORIES TO ADD/DELETE ========================
async def admin_all_subcategories(category, item_type):
    subcategories = await select_smm_subcategories(category) if item_type == "smm" \
        else await select_product_subcategories(category)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for subcategory in subcategories:
        keyboard.insert(InlineKeyboardButton(text=subcategory[2], callback_data=f"adm_sub:{subcategory[1]}"))
    keyboard.insert(InlineKeyboardButton(text="🔙Назад", callback_data="back_admin"))
    return keyboard


async def admin_edit_subcategories(category, item_type):
    subcategories = await select_smm_subcategories(category) if item_type == "smm" \
        else await select_product_subcategories(category)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for subcategory in subcategories:
        keyboard.add(InlineKeyboardButton(text=subcategory[2], callback_data=f"adm_sub:{subcategory[1]}"))
    keyboard.add(InlineKeyboardButton(text="📝Изменить название",
                                      callback_data=f"edit_button_arg:category:{category}:name"))
    keyboard.insert(InlineKeyboardButton(text="🗑Удалить", callback_data=f"delete_button:category:{category}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_admin"))
    return keyboard


# ======================== ITEMS TO EDIT/DELETE ========================
async def admin_items_menu(subcategory, item_type):
    items = await select_items(subcategory) if item_type == "smm" else await select_product_items(subcategory)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for item in items:
        if item_type == "smm":
            keyboard.add(InlineKeyboardButton(text=item[0], callback_data=f"adm_item:{item[8]}"))
        else:
            keyboard.add(InlineKeyboardButton(text=item[2], callback_data=f"adm_item:{item[3]}"))
    keyboard.add(InlineKeyboardButton(text="📝Изменить название",
                                      callback_data=f"edit_button_arg:sub:{subcategory}:name"))
    keyboard.insert(InlineKeyboardButton(text="🗑Удалить", callback_data=f"delete_button:sub:{subcategory}"))
    if item_type == "product":
        product_sub = await select_product_subcategory(subcategory)
        keyboard.add(InlineKeyboardButton(text="📝Изменить описание",
                                          callback_data=f"edit_button_arg:sub:{subcategory}:desc"))
        keyboard.insert(InlineKeyboardButton(text="📝Изменить цену",
                                             callback_data=f"edit_button_arg:sub:{subcategory}:cost"))
        keyboard.add(InlineKeyboardButton(text=f"{'🗂' if product_sub[5] == 'file' else '📧'}Тип продажи: "
                                               f"{'Файл' if product_sub[5] == 'file' else 'Текст'}",
                                          callback_data=f"edit_sell_type:{subcategory}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_admin"))
    return keyboard


# ======================== EDIT ITEM MARKUP ========================

async def edit_item_menu(item_id, item_type):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝Изменить название",
                                     callback_data=f"edit_button_arg:item:{item_id}:name")
            ] if item_type == "smm" else [],
            [
                InlineKeyboardButton(text="🆔 Изменить ID ", callback_data=f"edit_button_arg:item:{item_id}:id"),
                InlineKeyboardButton(text="📝Изменить описание", callback_data=f"edit_button_arg:item:{item_id}:desc")
            ] if item_type == "smm" else [],
            [
                InlineKeyboardButton(text="💰Изменить цену", callback_data=f"edit_button_arg:item:{item_id}:cost"),
                InlineKeyboardButton(text="🌀Изменить количество",
                                     callback_data=f"edit_button_arg:item:{item_id}:count")
            ] if item_type == "smm" else [],
            [
                InlineKeyboardButton(text="🗑Удалить", callback_data=f"delete_button:item:{item_id}")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
            ]
        ]
    )
    return keyboard


# MAIL MARKUP
async def mails_menu():
    mails = await select_all_mails()
    keyboard = InlineKeyboardMarkup(row_width=2)
    mail_type = {
        "smm": "📊 Накрутка ",
        "product": "📦 Товар ",
        "payment": "💳 Оплата ",
        "other": "❓Другой вопрос "
    }
    for mail in mails:
        keyboard.insert(InlineKeyboardButton(text=mail_type.get(mail[1]), callback_data=f"adm_help:{mail[0]}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_admin"))
    return keyboard


# MAIL MARKUP
async def in_mail_menu(user_id):
    mail = await select_mail(user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➡️Ответить", callback_data=f"help_reply:{mail[0]}")
            ],
            [
                InlineKeyboardButton(text="🗑Удалить", callback_data=f"help_del:{mail[0]}")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data="back_admin")
            ]
        ]
    )
    return keyboard
