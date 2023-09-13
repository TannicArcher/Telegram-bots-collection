import os
import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.general_menu import back_to_main_menu
from keyboards.inline.catalog_menu import *

from loader import dp, bot
from states.states import CatalogStates
from utils.db_api.db_commands import select_user, update_bal, \
    insert_order, add_bought, select_item, add_wasted, update_order_count, \
    select_settings, select_product_subcategory, select_product_items, del_product_item, add_smm_bought
from utils.nakrytka_api import add_order

# ========================SHOW ALL CATEGORIES========================
from utils.other_utils import send_to_all_admins


@dp.callback_query_handler(text="catalog", state="*")
async def show_categories(call: CallbackQuery, state: FSMContext):
    await state.finish()
    item_type = "product"
    await call.message.edit_caption("<b><i>💈Выберите интересующую вас категорию:</i></b>",
                                    reply_markup=await category_menu(item_type))
    await CatalogStates.CS1.set()
    await state.update_data(item_type=item_type)


# ========================SHOW SMM CATEGORIES========================
@dp.callback_query_handler(text="smm_catalog", state="*")
async def show_categories(call: CallbackQuery, state: FSMContext):
    await state.finish()
    item_type = "smm"
    await call.message.edit_caption("<b><i>💈Выберите интересующую вас категорию:</i></b>",
                                    reply_markup=await category_menu(item_type))
    await CatalogStates.CS1.set()
    await state.update_data(item_type=item_type)


# ========================SHOW ALL SUBCATEGORIES FROM THIS CATEGORY========================
@dp.callback_query_handler(text_startswith="category:", state="*")
async def inside_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_type = data.get("item_type")
    category_name = call.data.split(":")[1]
    await CatalogStates.CS2.set()
    await state.update_data(category_name=category_name)
    await call.message.edit_caption("<b><i>💈Выберите интересующую вас под-категорию:</i></b>",
                                    reply_markup=await sub_category_menu(category_name, item_type))


# ========================SHOW ALL ITEMS FROM THIS SUBCATEGORY========================
@dp.callback_query_handler(text_startswith="subcategory:", state="*")
async def inside_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_name, item_type = data.get("category_name"), data.get("item_type")
    sub_id = call.data.split(":")[1]
    await CatalogStates.CS3.set()
    await state.update_data(sub_id=sub_id)
    if item_type == "smm":
        await call.message.edit_caption("<b><i>💈Выберите интересующую вас услугу:</i></b>",
                                        reply_markup=await items_menu(sub_id, category_name))
    else:
        subcategory = await select_product_subcategory(sub_id)
        items = await select_product_items(sub_id)
        await call.message.edit_caption(f"<b>📦Товар: {subcategory[2]}\n"
                                        f"➖➖➖➖➖➖➖\n"
                                        f"📜Описание: \n{subcategory[3]}\n"
                                        f"➖➖➖➖➖➖➖\n"
                                        f"♻️Количество: {len(items)}\n"
                                        f"➖➖➖➖➖➖➖\n"
                                        f"💳Цена за 1 товар: {subcategory[4]} RUB</b>",
                                        reply_markup=await buy_product_menu(sub_id))


@dp.callback_query_handler(text_startswith="buy_product:", state="*")
async def buy_this_product(call: CallbackQuery, state: FSMContext):
    sub_id = call.data.split(":")[1]
    subcategory, items = await select_product_subcategory(sub_id), await select_product_items(sub_id)
    user = await select_user(call.from_user.id)
    if len(items) == 0:
        await call.answer("❗️Товар закончился")
    else:
        if user[3] > subcategory[4]:
            await CatalogStates.CS4.set()
            msg_to_edit = await call.message.edit_caption("<b>Напишите количество, которое хотите купить:</b>",
                                                          reply_markup=back_to_main_menu)
            await state.update_data(msg_to_edit=msg_to_edit)
        else:
            await call.answer("❗У вас недостаточно средств.")


@dp.message_handler(state=CatalogStates.CS4)
async def buy_this_product(message: Message, state: FSMContext):
    data = await state.get_data()
    sub_id, msg_to_edit, count = data.get("sub_id"), data.get("msg_to_edit"), message.text
    subcategory, items = await select_product_subcategory(sub_id), await select_product_items(sub_id)
    user, settings = await select_user(message.from_user.id), await select_settings()
    await message.delete()
    try:
        if len(items) >= int(count):
            if int(count) > 0:
                item, amount_to_pay = random.choice(items), subcategory[4] * int(count)
                await update_bal(message.from_user.id, -amount_to_pay)
                if subcategory[5] == "text":
                    await msg_to_edit.edit_caption(f"<b>Поздравляем с приобретением товара!\n"
                                                   f"➖➖➖➖➖➖➖\n"
                                                   f"Ваш товар:\n"
                                                   f"{item[2]}</b>",
                                                   reply_markup=back_to_main_menu)
                else:
                    await msg_to_edit.edit_caption(f"<b>🎉 Поздравляем с приобретением товара!\n"
                                                   f"➖➖➖➖➖➖➖\n"
                                                   f"📦 Купленный товар:</b>",
                                                   reply_markup=back_to_main_menu)
                    with open(item[2], "rb") as file:
                        doc = file.read()
                    await message.answer_document(doc)
                    os.remove(item[2])
                await del_product_item(item[3])
                await insert_order(user_id=message.from_user.id, item_name=subcategory[2], count=count, url=None,
                                   order_id=None, payed=amount_to_pay, order_type="product")
                await add_wasted(amount_to_pay)
                await update_order_count()
                await add_bought(message.from_user.id)
                await state.finish()
                await bot.send_message(settings[4], f"<b>📦 Сделана покупка</b>\n\n"
                                                    f"<i>🧿Товар: {subcategory[2]}\n"
                                                    f"♻️Количество: {count}\n"
                                                    f"💳Общая стоимость: {amount_to_pay}\n"
                                                    f"👾Пользователь: @{message.from_user.username}\n"
                                                    f"🆔ID: {message.from_user.id}</i>")
            else:
                await msg_to_edit.edit_caption("<b>❗️Не верное количество.\n"
                                               "Напишите количество, которое хотите купить:</b>",
                                               reply_markup=back_to_main_menu)
        else:
            await msg_to_edit.edit_caption("<b>❗️Вы ввели количество товара больше, чем есть в наличии.\n"
                                           "Напишите количество, которое хотите купить:</b>",
                                           reply_markup=back_to_main_menu)
    except ValueError:
        await msg_to_edit.edit_caption("<b>❗️Не верное количество.\n"
                                       "Напишите количество, которое хотите купить:</b>",
                                       reply_markup=back_to_main_menu)


# ========================SHOW ITEM========================
@dp.callback_query_handler(text_startswith="item:", state="*")
async def inside_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_name, sub_id = data.get("category_name"), data.get("sub_id")
    item_name = call.data.split(":")[1]
    item = await select_item(item_name)
    await CatalogStates.CS4.set()
    await state.update_data(item=item)
    await call.message.edit_caption(f"{item[7]}\n\n<b><i>Минимальное количество:</i></b> <code>{item[4]}</code>\n"
                                    f"<b><i>Максимальное количество:</i></b> <code>{item[5]}</code>\n\n"
                                    f"<b><i>Цена за {item[4]}:</i></b> <code>{item[3]}</code>",
                                    reply_markup=in_item_menu(item_name, sub_id))


@dp.callback_query_handler(text="calc", state=CatalogStates.CS4)
async def calc(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item = data.get("item")

    msg_to_edit = await call.message.edit_caption(f"💳Введите желаемое количество для расчета цены:",
                                                  reply_markup=await calc_menu(item[8]))
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=CatalogStates.CS4)
async def calc(message: Message, state: FSMContext):
    data = await state.get_data()
    item, msg_to_edit = data.get("item"), data.get("msg_to_edit")
    user = await select_user(message.from_user.id)
    await message.delete()
    try:
        num = int(message.text)
        if item[5] >= num > 0:
            if num >= item[4]:
                cost = round(item[3] / item[4] * num)
                balance_after_pay = user[3] - cost
                if user[3] >= cost:
                    await msg_to_edit.edit_caption(f"<b><i>💰Ваш баланс сейчас: {user[3]}\n"
                                                   f"💳Спишется: {cost}\n"
                                                   f"💸Останется: {balance_after_pay}</i></b>",
                                                   reply_markup=await calc_menu(item[8]))
                    await state.finish()
                else:
                    await msg_to_edit.edit_caption(f"<b>У вас недостаточно средств.</b>",
                                                   reply_markup=await calc_menu(item[8]))
            else:
                await msg_to_edit.edit_caption(f"<b>Не верное количество (указанно меньше минимального),"
                                               f" попробуйте еще раз</b>", reply_markup=await calc_menu(item[8]))
        else:
            await msg_to_edit.edit_caption(f"<b>Не верное количество "
                                           f"(Количество не может быть меньше нуля и привышать максимальное количетсво)"
                                           f", попробуйте еще раз</b>", reply_markup=await calc_menu(item[8]))

    except ValueError:
        await msg_to_edit.edit_caption(f"<b>Не верное количество (Количество должно состоять из цифр),"
                                       f" попробуйте еще раз</b>", reply_markup=await calc_menu(item[8]))


# ========================BUY SELECTED ITEM========================
# ASK FOR COUNT
@dp.callback_query_handler(text_startswith="buy_this_item:", state=CatalogStates.CS4)
async def buy(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item = data.get("item")
    user = await select_user(call.from_user.id)
    cost = item[3] / item[4]
    amount = round(user[3] / cost)
    await call.message.edit_caption(f"<b>✔️Вы выбрали услугу: <code>{item[0]}</code>\n\n"
                                    f"💰Вашего баланса хватит на: <code>{amount}</code>\n\n"
                                    f"👉Введите количество которое хотите купить:</b>", reply_markup=back_to_main_menu)
    await state.update_data(msg_to_edit=call.message)
    await CatalogStates.CS5.set()


# ASK FOR URL
@dp.message_handler(state=CatalogStates.CS5)
async def receive_count(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, item = data.get("msg_to_edit"), data.get("item")
    await message.delete()
    try:
        count = int(message.text)
        user = await select_user(message.from_user.id)
        if item[4] <= count <= item[5]:
            count_to_pay = round(item[3] / item[4] * count)
            if count_to_pay <= user[3]:
                await state.update_data(count=count, count_to_pay=count_to_pay)
                await msg_to_edit.edit_caption(
                    f"<b>♦️Вы ввели количество: {count}\n\n"
                    f"💰С вашего баланса будет списано: <code>{count_to_pay}</code> Rub\n\n"
                    f"💰Ваш баланс станет: <code>{user[3] - count_to_pay}</code> Rub\n\n"
                    f"👉Введите ссылку:</b>",
                    parse_mode="HTML", reply_markup=back_to_main_menu)
                await CatalogStates.CS6.set()
            else:
                await msg_to_edit.edit_caption(f"<b>У вас недостаточно средств для совершения этой операции.</b>\n"
                                               f"<code>От {item[4]} до {item[5]}</code>\n"
                                               f"Цена за {item[4]}: <code>{item[3]}</code>\n"
                                               f"<b>Введите количество заказа</b>⤵",
                                               parse_mode="HTML", reply_markup=back_to_main_menu)
        else:
            await msg_to_edit.edit_caption(f"<b>Количество меньше/больше допустимого.</b>\n"
                                           f"<code>От {item[4]} до {item[5]}</code>\n"
                                           f"Цена за {item[4]}: <code>{item[3]}</code>\n"
                                           f"<b>Введите количество заказа</b>⤵",
                                           parse_mode="HTML", reply_markup=back_to_main_menu)
    except ValueError:
        await msg_to_edit.edit_caption(f"<b>Неверное количество</b>"
                                       f"<code>От {item[4]} до {item[5]}</code>\n"
                                       f"Цена за {item[4]}: <code>{item[3]}</code>\n"
                                       f"<b>Введите количество заказа</b>⤵",
                                       parse_mode="HTML", reply_markup=back_to_main_menu)


# START THIS ORDER
@dp.message_handler(state=CatalogStates.CS6)
async def receive_count(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, count_to_pay, item = data.get("msg_to_edit"), int(data.get("count_to_pay")), data.get("item")
    count, settings = data.get("count"), await select_settings()
    url = message.text
    await message.delete()
    if "http" in url:
        await msg_to_edit.edit_caption(f"<b>⚠️Проверьте введённые данные⚠️\n\n"
                                       f"🔗Ссылка: <code>{url}</code>\n"
                                       f"♦️Количество: <code>{count}</code>\n\n"
                                       f"🔥Если вы готовы сделать заказ нажмите на кнопку снизу!</b>",
                                       reply_markup=accept_order_menu)
        await state.update_data(url=url)
        await CatalogStates.next()
    else:
        await msg_to_edit.edit_caption(f"<b>Не верный формат ссылки, попробуйте еще раз</b>",
                                       reply_markup=back_to_main_menu)


# START THIS ORDER
@dp.callback_query_handler(state=CatalogStates.CS7, text_startswith="order_a:")
async def receive_count(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, count_to_pay, item = data.get("msg_to_edit"), int(data.get("count_to_pay")), data.get("item")
    count, url = data.get("count"), data.get("url")
    user, settings = await select_user(call.from_user.id), await select_settings()
    bal_past = user[3]
    await call.message.delete()
    with open("main_menu.jpg", "rb") as file:
        photo = file.read()
    if call.data.split(":")[-1] == "accept":
        try:
            request = add_order(item[6], url, count)
            if request.get("error") == "You have active order with this link. Please wait until " \
                                       "order being completed.":
                await call.message.answer_photo(photo=photo, caption=f"<b>✅На эту ссылку уже есть активный заказ.</b>\n"
                                                                     f"Ваш баланс не был списан.",
                                                parse_mode="HTML", reply_markup=back_to_main_menu)
            else:
                await call.message.answer_photo(photo=photo, caption=f"<b>✅Ваш заказ успешно начал выполнение\n\n"
                                                                     f"🔑Номер вашего заказа - <code>{request['order']}</code>\n"
                                                                     f"➖➖➖➖➖➖➖➖➖\n"
                                                                     f"❤️Спасибо что выбираете нас</b>",
                                                reply_markup=after_order_menu)
                await update_bal(call.from_user.id, -count_to_pay)
                await add_wasted(count_to_pay)
                await update_order_count()
                await add_smm_bought()
                await add_bought(call.from_user.id)
                await insert_order(user_id=call.from_user.id, item_name=item[0], count=count, url=url,
                                   order_id=request['order'], payed=count_to_pay, order_type="smm")
                user = await select_user(call.from_user.id)
                await bot.send_message(settings[4], f"""              
<b>🛒 Куплена накрутка</b>

<i>◽️Ссылка: {url}
◽️Цена: {count_to_pay}
◽️Количество: {count}
◽️Пользователь: @{call.from_user.username}
◽️Айди заказчика: {call.from_user.id}
◽️Баланс был: {bal_past}
◽️Баланс стал: {user[3]}
◽️Услуга: {item[0]}
◽️Айди услуги: {item[8]}</i>
""")
        except KeyError:
            await call.message.answer_photo(photo=photo, caption=f"<b>Приносим свои извинения, произошла ошибка,"
                                                                 f" ваш баланс не был списан.</b>",
                                            reply_markup=back_to_main_menu)
            await bot.send_message(settings[6], f"📛ОШИБКА📛\n"
                                                f"Человек @{call.from_user.username} сделал заказ:\n"
                                                f"Услуга: {item[0]}\n"
                                                f"Количество: {count}\n"
                                                f"Ссылка: {url}\n"
                                                f"Но на счету api недостаточно средств для его выполнения.\n"
                                                f"<b>Баланс человека не был списан.</b>")
            await state.finish()
