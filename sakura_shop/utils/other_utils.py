from data.config import ADMINS
from loader import bot


async def send_to_all_admins(text, markup=None):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, text, reply_markup=markup)
        except Exception as e:
            print(e)
            continue


async def get_main_menu_pic():
    with open("main_menu.jpg", "rb") as file:
        photo = file.read()
    return photo
