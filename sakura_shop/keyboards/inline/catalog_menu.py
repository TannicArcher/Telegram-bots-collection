from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import select_items, select_sub_category, select_categories, select_smm_subcategories, \
    select_product_subcategories

# ======================== CHECK AGREE ========================
accept_order_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫Отменить", callback_data="back_to_main_menu"),
            InlineKeyboardButton(text="✅ Заказать", callback_data="order_a:accept")
        ]
    ]
)

# ======================== TO MAIN MENU ========================
after_order_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐️ Главное меню ⭐️", callback_data="show_main_menu")
        ]
    ]
)


# ======================== MARKUP IN THE ITEM ========================
def in_item_menu(item_name, subcategory):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔰Заказать🔰", callback_data=f"buy_this_item:{item_name}")
            ],
            [
                InlineKeyboardButton(text="⚙️Калькулятор", callback_data=f"calc")
            ],
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data=f"subcategory:{subcategory}")
            ]
        ]
    )
    return keyboard


# ======================== CATEGORY ========================
async def category_menu(category_type):
    categories = await select_categories(category_type)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        keyboard.insert(InlineKeyboardButton(text=category[0], callback_data=f"category:{category[1]}"))
    if category_type == "product":
        keyboard.add(InlineKeyboardButton(text="⭐️ Накрутка ⭐️", callback_data="smm_catalog"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_to_main_menu"
                                      if category_type == "product" else "catalog"))
    return keyboard


# ======================== SUBCATEGORY ========================
async def sub_category_menu(category, item_type):
    subcategories = await select_smm_subcategories(category) if item_type == "smm" \
        else await select_product_subcategories(category)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for subcategory in subcategories:
        keyboard.insert(InlineKeyboardButton(text=subcategory[2], callback_data=f"subcategory:{subcategory[1]}"))
    keyboard.insert(InlineKeyboardButton(text="🔙Назад", callback_data="catalog"))
    return keyboard


async def buy_product_menu(sub_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛒 Купить 🛒", callback_data=f"buy_product:{sub_id}")
            ],
            [
                InlineKeyboardButton(text="❌Отмена", callback_data="back_to_main_menu")
            ]
        ]
    )
    return keyboard


# ======================== ITEMS ========================
async def items_menu(subcategory, category):
    items = await select_items(subcategory)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in items:
        keyboard.insert(InlineKeyboardButton(text=item[0], callback_data=f"item:{item[8]}"))
    keyboard.insert(InlineKeyboardButton(text="🔙Назад", callback_data=f"category:{category}"))
    return keyboard


# ======================== CALC MARKUP ========================
async def calc_menu(item_name):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️Назад", callback_data=f"item:{item_name}")
            ]
        ]
    )
    return keyboard
