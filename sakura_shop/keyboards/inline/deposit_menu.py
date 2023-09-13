import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import select_settings


payment_methods_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💳 QIWI P2P", callback_data="payment_method:p2p")
        ],
        [
            InlineKeyboardButton(text="💳 QIWI По номеру ", callback_data="payment_method:num")
        ],
        [
            InlineKeyboardButton(text="🔙Назад", callback_data="back_to_main_menu")
        ]
    ]
)


# CHECK PAYMENT
async def check_menu(cost, user_id, pay_type, date):
    settings = await select_settings()
    chars, bill_id = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', ''
    url = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={settings[0]}&" \
          f"amountInteger={cost}&amountFraction=0&extra%5B%27comment%27%5D={user_id}&" \
          f"currency=643&blocked[0]=account&blocked[1]=comment&blocked[2]=sum" if pay_type == "num" else \
        f"https://oplata.qiwi.com/create?" \
        f"publicKey={settings[2]}" \
        f"&amount={cost}" \
        f"&lifetime={date}" \
        f"&comment={user_id}" \
        f"&billId={bill_id}"

    for i in range(15):
        bill_id += random.choice(chars)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌟 Оплатить 🌟",
                    url=url
                )
            ],
            [
                InlineKeyboardButton(text="✅ Я оплатил", callback_data="check"),
                InlineKeyboardButton(text="🚫 Отменить", callback_data="back_to_main_menu")
            ],
            [
                InlineKeyboardButton(text="🆘 Помощь", url="https://t.me/GREENADMINSHOP")
            ]
        ]
    )
    return markup, bill_id, url
