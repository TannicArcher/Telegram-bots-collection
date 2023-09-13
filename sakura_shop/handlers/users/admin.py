import asyncio
import os
import random

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import BadRequest

from filters import IsAdmin
from keyboards.inline.admin_menu import *
from loader import dp, bot
from states.admin_states import *
from utils.db_api.db_commands import *
from utils.nakrytka_api import get_balance
from utils.other_utils import get_main_menu_pic
from utils.qiwi import balance


@dp.callback_query_handler(IsAdmin(), text="back_admin", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        await call.message.edit_caption(f"<b>👑 Админ панель!</b>\n",
                                        reply_markup=admin_menu)
    except BadRequest:
        photo = await get_main_menu_pic()
        await call.message.delete()
        await call.message.answer_photo(photo=photo, caption=f"<b>👑 Админ панель!</b>",
                                        reply_markup=admin_menu)


@dp.callback_query_handler(text="help", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_caption(f"Выберите запрос:",
                                    reply_markup=await mails_menu())


@dp.callback_query_handler(text_startswith="adm_help:")
async def support(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    mail = await select_mail(user_id)
    mail_type = {
        "smm": "📊 Накрутка ",
        "product": "📦 Товар ",
        "payment": "💳 Оплата ",
        "other": "❓Другой вопрос "
    }
    await call.message.edit_caption(f"<b>Запрос:\n\n"
                                    f"Тип запроса: {mail_type.get(mail[1])}\n"
                                    f"ID юзера: {mail[0]}\n"
                                    f"Сообщение: \n{mail[2]}</b>",
                                    reply_markup=await in_mail_menu(user_id))


@dp.callback_query_handler(text_startswith="help_del:")
async def support(call: CallbackQuery):
    user_id = call.data.split(":")[1]
    await del_mail(user_id)
    await call.message.edit_caption(f"Выберите запрос:",
                                    reply_markup=await mails_menu())


@dp.callback_query_handler(text_startswith="help_reply:")
async def support(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    msg_to_edit = await call.message.edit_caption(f"Напишите ответ:",
                                                  reply_markup=back_admin)
    await SOSAdminStates.SS1.set()
    await state.update_data(msg_to_edit=msg_to_edit, user_id=user_id)


@dp.message_handler(state=SOSAdminStates.SS1)
async def support(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id, msg_to_edit = data.get("user_id"), data.get("msg_to_edit")
    mail = await select_mail(user_id)
    mail_type = {
        "smm": "📊 Накрутка ",
        "product": "📦 Товар ",
        "payment": "💳 Оплата ",
        "other": "❓Другой вопрос "
    }
    await message.delete()
    await del_mail(user_id)
    await msg_to_edit.edit_caption(f"Ответ отправлен\n\nВыберите запрос:",
                                   reply_markup=await mails_menu())
    await bot.send_message(user_id, f"<b>🌿Ваш запрос в поддержку был обработан:\n\n"
                                    f"🍃Тип запроса: {mail_type.get(mail[1])}\n"
                                    f"🌪Запрос: \n{mail[2]}\n\n"
                                    f"🔥Ответ: \n{message.text}</b>", reply_markup=broadcast_menu)
    await state.finish()


@dp.callback_query_handler(text="admin_stat")
async def edit_commission(call: CallbackQuery):
    users, stat = await select_all_users(), await select_stat()
    users_balance_now = 0
    users_balance_all = 0
    users_with_ball = 0
    for user in users:
        users_balance_now += user[3]
        users_balance_all += user[2]
        if user[3] != 0:
            users_with_ball += 1
    await call.message.edit_caption(f'<b>📊 Статистика бота: \n\n'
                                    f'👤Пользователей: <code>{len(users)}</code>\n'
                                    f'💳Купленно товаров: <code>{stat[2]}</code>\n'
                                    f'🔥Пополнили баланс: <code>{stat[1]}</code>\n'
                                    f'🧿Сумма накрутки: <code>{stat[0]}</code>\n'
                                    f'➖➖➖➖➖➖➖➖➖➖\n'
                                    f"💰Баланс киви: <code>{await balance()}</code> RUB\n"
                                    f"💰Баланс smm panel: <code>{get_balance()}</code> RUB</b>",
                                    reply_markup=back_admin)


@dp.callback_query_handler(text="get_user")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_caption("<b>🆔Введите его ID:</b>",
                                                  reply_markup=back_admin)
    await GetUserState.GU1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=GetUserState.GU1)
async def receive_com(message: Message, state: FSMContext):
    user_id = message.text
    data = await state.get_data()
    msg_to_edit, user = data.get("msg_to_edit"), await select_user(user_id)
    await message.delete()
    chat = await bot.get_chat(user_id)
    await GetUserState.next()
    await state.update_data(user_db=user)
    await msg_to_edit.edit_caption(f"<b>💰Баланс: {user[3]}\n"
                                   f"📦Куплено товаров: {user[1]}\n"
                                   f"💳Сумма пополнений: {user[2]}\n"
                                   f"🎁Бонус к пополнению: {user[6]}\n"
                                   f"👨Пользователь: @{chat.username}\n"
                                   f"🆔ID Юзера: {user_id}</b>",
                                   reply_markup=get_user_menu)


@dp.callback_query_handler(text="ref_list", state=GetUserState.GU2)
async def edit_bonus(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data.get("user_db")
    user, refs = await select_user(user[0]), await select_all_refs(user[0])
    username_list = []
    for ref in refs:
        info = await bot.get_chat(ref[0])
        username_list.append(f"@{info.username}")
    ref_text = "\n".join(username_list)
    await call.message.edit_caption(f"<b>{ref_text}</b>", reply_markup=back_admin)


@dp.callback_query_handler(text="edit_bonus", state=GetUserState.GU2)
async def edit_bonus(call: CallbackQuery):
    await GetUserState.next()
    await call.message.edit_caption(f"<b><i>Напишите новый бонус</i></b>", reply_markup=back_admin)


@dp.message_handler(state=GetUserState.GU3)
async def receive_bonus(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, user = data.get("msg_to_edit"), data.get("user_db")
    await message.delete()
    try:
        bonus = int(message.text)
        await update_bonus(user[0], bonus)
        await state.finish()
        await GetUserState.GU2.set()
        user = await select_user(user[0])
        await state.update_data(user_db=user, msg_to_edit=msg_to_edit)
        chat = await bot.get_chat(user[0])
        await msg_to_edit.edit_caption(f"<b>💰Баланс: {user[3]}\n"
                                       f"📦Куплено товаров: {user[1]}\n"
                                       f"💳Сумма пополнений: {user[2]}\n"
                                       f"🎁Бонус к пополнению: {user[6]}\n"
                                       f"👨Пользователь: @{chat.username}\n"
                                       f"🆔ID Юзера: {user[0]}</b>",
                                       reply_markup=get_user_menu)
    except ValueError:
        await msg_to_edit.edit_caption("<b>Не верный формат, попробуйте еще раз</b>", reply_markup=back_admin)


@dp.callback_query_handler(text="broadcast")
async def broadcast2(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_caption("<b>Отправь фото с текстом, которые будут рассылаться по юзерам\n"
                                                  "Можно просто текст</b>",
                                                  reply_markup=back_admin)
    await BroadcastState.BS1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(content_types=['photo', 'text'], state=BroadcastState.BS1)
async def broadcast4(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, easy_chars = data.get("msg_to_edit"), 'abcdefghijklnopqrstuvwxyz1234567890'
    await message.delete()
    if message.photo:
        name = ''
        for i in range(10):
            name += random.choice(easy_chars)
        photo_name = name + ".jpg"
        await message.photo[-1].download(photo_name)
        os.rename(photo_name, f"photos/{photo_name}")
        await state.update_data(photo=photo_name, text=message.caption)
        await asyncio.sleep(2)
        path = f'photos/{photo_name}'
        await msg_to_edit.delete()
        with open(path, 'rb') as f:
            photo = f.read()
        await message.answer_photo(photo=photo, caption=f"{message.caption}\n\n"
                                                        f"<b>Все правильно? Отправляем?</b>",
                                   reply_markup=choose_menu)
    else:
        await state.update_data(text=message.text)
        await msg_to_edit.edit_caption(message.text + "\n\n<b>Все правильно? Отправляем?</b>", reply_markup=choose_menu)
    await BroadcastState.next()


@dp.callback_query_handler(text="yes", state=BroadcastState.BS2)
async def broadcast_text_post(call: CallbackQuery, state: FSMContext):
    users = await select_all_users()
    data = await state.get_data()
    text, photo_name = data.get("text"), data.get('photo')
    await state.finish()
    await call.message.delete()
    msg_to_delete = await call.message.answer("<b>Рассылка начата</b>")
    if photo_name is None:
        for user in users:
            try:
                await bot.send_message(user[0], text, parse_mode="HTML")
            except Exception as e:
                print(e)
                continue
    else:
        path = f'photos/{photo_name}'
        with open(path, 'rb') as f:
            photo = f.read()
        for user in users:
            try:
                await bot.send_photo(chat_id=user[0], photo=photo, caption=text, parse_mode="HTML")
            except Exception as e:
                print(e)
                continue
        os.remove(path)
    await msg_to_delete.delete()
    await call.message.answer("<b>Рассылка закончена</b>", reply_markup=back_admin)


@dp.callback_query_handler(text="no", state=BroadcastState.BS2)
async def broadcast_text_post(call: CallbackQuery, state: FSMContext):
    if not call.message.photo:
        await call.message.edit_text("Админ-меню", reply_markup=admin_menu)
    else:
        await call.message.delete()
        await call.message.answer("Админ-меню", reply_markup=admin_menu)
    await state.finish()


# ========================ADDING BALANCE========================
# ASK FOR ID
@dp.callback_query_handler(text_startswith="balance:")
async def admin_give_bal(call: CallbackQuery, state: FSMContext):
    operation = call.data.split(":")[1]
    await call.message.edit_caption(
        f"<b>Напишите id юзера, "
        f"{'которому хотите дать баланс' if operation == 'add' else 'у которого хотите забрать баланс'}</b>",
        parse_mode="HTML", reply_markup=back_admin)
    await GiveBalState.GB1.set()
    await state.update_data(msg_to_edit=call.message)
    await state.update_data(operation=operation)


# ASK FOR AMOUNT OF BALANCE
@dp.message_handler(state=GiveBalState.GB1)
async def admin_give_bal(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, operation = data.get("msg_to_edit"), data.get("operation")
    user_id = message.text
    user = await select_user(user_id)
    await message.delete()
    if user is not None:
        await msg_to_edit.edit_caption(f"<b>Напишите сумму, которую нужно"
                                       f" {'добавить юзеру' if operation == 'add' else 'забрать у юзера'}</b>",
                                       parse_mode="HTML", reply_markup=back_admin)
        await state.update_data(user_id=user_id)
        await GiveBalState.next()
    else:
        await msg_to_edit.edit_caption(f"<b>Юзер с данным id (<code>{user_id}</code>) - не найден\n"
                                       f"Попробуйте еще раз</b>", parse_mode="HTML", reply_markup=back_admin)


# GIVE BALANCE
@dp.message_handler(state=GiveBalState.GB2)
async def admin_give_bal(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    msg_to_edit, user_id, operation = data.get("msg_to_edit"), data.get("user_id"), data.get("operation")
    try:
        bal_to_add = int(message.text)
        await update_bal(user_id, bal_to_add if operation == "add" else -bal_to_add)
        await msg_to_edit.edit_caption(f"Баланс в размере <code>{bal_to_add}руб</code> был "
                                       f"{'начислен юзеру' if operation == 'add' else 'отнят у юзера'} с ID"
                                       f" - <code>{user_id}</code>", reply_markup=back_admin)
        await state.finish()
    except ValueError:
        await msg_to_edit.edit_caption("<b>Произошла ошибка, возможно вы указали неверное количество.\n"
                                       "Попробуйте еще раз</b>", parse_mode="HTML", reply_markup=back_admin)


# ======================== EDIT ========================
@dp.callback_query_handler(text_startswith="edit_sell_type:", state="*")
async def get_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_type = data.get("item_type")
    id_arg = call.data.split(":")[1]
    items = await select_product_items(id_arg)
    if len(items) == 0:
        subcategory = await select_product_subcategory(id_arg)
        await update_file_type(id_arg, "file" if subcategory[5] == "text" else 'text')
        subcategory = await select_product_subcategory(id_arg)
        await call.message.edit_caption(f"Подкатегория: <code>{subcategory[2]}</code>",
                                        reply_markup=await admin_items_menu(id_arg, item_type))
    else:
        await call.answer("❗Прежде чем менять тип продажи, пожалуйста удалите все товары,"
                          " существующие в этой подкатегории", show_alert=True)


# DELETE
@dp.callback_query_handler(text_startswith="delete_button:", state="*")
async def get_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_type = data.get("item_type")
    button_type, id_arg = call.data.split(":")[1], call.data.split(":")[2]
    if button_type == "category":
        text = "Категория удаленна!"
        await del_category(id_arg, item_type)
    elif button_type == "sub":
        text = "Подкатегория удаленна!"
        if item_type == "smm":
            await del_sub_category(id_arg)
        else:
            await del_product_subcategory(id_arg)
    else:
        if item_type == "smm":
            text = "Услуга удаленна!"
            await del_item(id_arg)
        else:
            text = "Товар удален!"
            await del_product_item(id_arg)
    await call.message.edit_caption(text,
                                    reply_markup=back_admin)


# EDIT NAME
@dp.callback_query_handler(text_startswith="edit_button_arg:", state="*")
async def get_category(call: CallbackQuery, state: FSMContext):
    button_type, id_arg, edit_arg = call.data.split(":")[1], call.data.split(":")[2], call.data.split(":")[3]
    msg_to_edit = await call.message.edit_caption("Напишите новый аргумент:",
                                                  reply_markup=back_admin)
    await state.update_data(button_type=button_type, id_arg=id_arg, msg_to_edit=msg_to_edit, edit_arg=edit_arg)


@dp.message_handler(state=EditButtonState)
async def edit_name_func(message: Message, state: FSMContext):
    data = await state.get_data()
    item_type, button_type, id_arg = data.get("item_type"), data.get("button_type"), data.get("id_arg")
    msg_to_edit, edit_arg = data.get("msg_to_edit"), data.get("edit_arg")
    await message.delete()
    if edit_arg == "name":
        if button_type == "category":
            await update_category_name(id_arg, message.text)
            category = await select_category(id_arg)
            await msg_to_edit.edit_caption(f"<b>Название измененно!</b>\n"
                                           f"Категория: <code>{category[0]}</code>",
                                           reply_markup=await admin_edit_subcategories(id_arg, item_type))
        elif button_type == "sub":
            if item_type == "smm":
                await update_sub_name_smm(id_arg, message.text)
                subcategory = await select_sub_category(id_arg)
            else:
                await update_sub_name_product(id_arg, message.text)
                subcategory = await select_product_subcategory(id_arg)
            await msg_to_edit.edit_caption(f"<b>Название измененно!</b>\n"
                                           f"Подкатегория: <code>{subcategory[2]}</code>",
                                           reply_markup=await admin_items_menu(id_arg, item_type))
        elif button_type == "item":
            await update_item_name(id_arg, message.text)
            item = await select_item(id_arg)
            await msg_to_edit.edit_caption(f"<b>Название измененно!</b>\n"
                                           f"Услуга: <code>{item[0]}</code>",
                                           reply_markup=await edit_item_menu(id_arg, item_type))

    elif edit_arg == "desc":
        if button_type == "sub":
            await update_sub_desc(id_arg, message.text)
            subcategory = await select_product_subcategory(id_arg)
            await msg_to_edit.edit_caption(f"<b>Описание измененно!</b>\n"
                                           f"Подкатегория: <code>{subcategory[2]}</code>",
                                           reply_markup=await admin_items_menu(id_arg, item_type))

        elif button_type == "item":
            await update_item_desc(id_arg, message.text)
            item = await select_item(id_arg)
            await msg_to_edit.edit_caption(f"<b>Описание измененно!</b>\n"
                                           f"Услуга: <code>{item[0]}</code>",
                                           reply_markup=await edit_item_menu(id_arg, item_type))

    elif edit_arg == "cost":
        try:
            cost = int(message.text)
            if button_type == "sub":
                await update_cost_product(id_arg, cost)
                subcategory = await select_product_subcategory(id_arg)
                await msg_to_edit.edit_caption(f"<b>Цена изменена!</b>\n"
                                               f"Подкатегория: <code>{subcategory[2]}</code>",
                                               reply_markup=await admin_items_menu(id_arg, item_type))

            elif button_type == "item":
                await update_cost(id_arg, cost)
                item = await select_item(id_arg)
                await msg_to_edit.edit_caption(f"<b>Цена изменена!</b>\n"
                                               f"Услуга: <code>{item[0]}</code>",
                                               reply_markup=await edit_item_menu(id_arg, item_type))
        except ValueError:
            await msg_to_edit.edit_caption(f"<b>Неверное значение.\nПопробуйте еще раз.</b>",
                                           reply_markup=back_admin)

    elif edit_arg == "id":
        item = await select_item(id_arg)
        await msg_to_edit.edit_caption(f"<b>ID услуги было изменено</b>\n"
                                       f"Услуга: <code>{item[0]}</code>",
                                       reply_markup=await edit_item_menu(id_arg, item_type))
        await update_service_id(item[8], message.text)

    elif edit_arg == "count":
        item = await select_item(id_arg)
        min_max = message.text.split(" ")
        if len(min_max) == 2:
            await msg_to_edit.edit_caption(f"<b>Количетсво было измененно</b>\n"
                                           f"Услуга: <code>{item[0]}</code>",
                                           reply_markup=await edit_item_menu(id_arg, item_type))
            await update_min(item[8], min_max[0])
            await update_max(item[8], min_max[1])
            await state.finish()
        else:
            await msg_to_edit.edit_caption(f"<b>Не верный формат, попробуйте еще раз</b>",
                                           reply_markup=back_admin)


# SHOW ALL ITEMS
@dp.callback_query_handler(text="edit_buttons")
async def admin_edit_cost(call: CallbackQuery):
    await call.message.edit_caption("Что будем менять?", reply_markup=edit_buttons_menu)


@dp.callback_query_handler(text_startswith="edit:")
async def admin_edit_cost(call: CallbackQuery, state: FSMContext):
    item_type = call.data.split(":")[1]
    await call.message.edit_caption("Что будем менять?", reply_markup=await admin_all_categories(item_type))
    await EditButtonState.EC1.set()
    await state.update_data(item_type=item_type)


@dp.callback_query_handler(text_startswith="adm_cat:", state=EditButtonState.EC1)
async def get_category(call: CallbackQuery, state: FSMContext):
    cat_id, data = call.data.split(":")[1], await state.get_data()
    category = await select_category(cat_id)
    item_type = data.get("item_type")
    await call.message.edit_caption(f"Категория: <code>{category[0]}</code>",
                                    reply_markup=await admin_edit_subcategories(cat_id, item_type))
    await EditButtonState.next()
    await state.update_data(cat_id=cat_id)


@dp.callback_query_handler(text_startswith="adm_sub:", state=EditButtonState.EC2)
async def get_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sub_id, item_type = call.data.split(":")[1], data.get("item_type")
    if item_type == "smm":
        subcategory = await select_sub_category(sub_id)
    else:
        subcategory = await select_product_subcategory(sub_id)
    await call.message.edit_caption(f"Подкатегория: <code>{subcategory[2]}</code>",
                                    reply_markup=await admin_items_menu(sub_id, item_type))
    await EditButtonState.next()
    await state.update_data(sub_id=sub_id)


@dp.callback_query_handler(text_startswith="adm_item:", state=EditButtonState.EC3)
async def get_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_id, item_type = call.data.split(":")[1], data.get("item_type")
    if item_type == "smm":
        item = await select_item(item_id)
        await call.message.edit_caption(f"<b><i>💎Услуга: {item[0]}\n\n"
                                        f"📝Описание услуги:\n{item[7]}\n\n"
                                        f"💵Цена за {item[4]}: {item[3]} RUB\n\n🌀Минимум: {item[4]}\n"
                                        f"🌀Максимум: {item[5]}\n\n🆔ID услуги: {item[6]}</i></b>",
                                        reply_markup=await edit_item_menu(item_id, item_type))
    else:
        item = await select_product_item(item_id)
        await call.message.edit_caption(f"<b>Товар: <code>{item[2]}</code></b>",
                                        reply_markup=await edit_item_menu(item_id, item_type))
    await EditButtonState.next()
    await state.update_data(item=item)


# ========================ADD/DELETE BUTTON========================
@dp.callback_query_handler(text="add")
async def buttons(call: CallbackQuery):
    await call.message.edit_caption("<b>Выберите тип:</b>",
                                    reply_markup=button_type_menu)


# ASK FOR TYPE OF BUTTON
@dp.callback_query_handler(text_startswith="add_button:")
async def buttons(call: CallbackQuery):
    operation = call.data.split(":")[1]
    await call.message.edit_caption("<b>Выберите тип:</b>",
                                    reply_markup=await add_button_type_menu(operation))


# CHOOSING TYPE OF BUTTON
@dp.callback_query_handler(text_startswith="button_type:")
async def add_buttons_main(call: CallbackQuery, state: FSMContext):
    button_type, item_type = call.data.split(":")[1], call.data.split(":")[2]
    # CATEGORY TYPE
    if button_type == "category":
        msg_to_edit = await call.message.edit_caption("<b>Напишите название категории</b>", reply_markup=back_admin)
        await AddCategory.AC1.set()
        await state.update_data(msg_to_edit=msg_to_edit)

    # SUBCATEGORY TYPE
    elif button_type == "subcategory":
        await call.message.edit_caption("<b>Выбери категорию, в которой будет находиться под-категорию</b>",
                                        reply_markup=await admin_all_categories(item_type))
        await AddSubCategory.ASC1.set()

    # ITEM TYPE
    elif button_type == "item":
        await call.message.edit_caption("<b>Выберите категорию, в которой будет находиться услуга</b>",
                                        reply_markup=await admin_all_categories(item_type))
        await AddItem.AI1.set()
    await state.update_data(item_type=item_type)


# ========================ADD CATEGORY========================
# RECEIVE NAME OF THE CATEGORY AND ADD IT
@dp.message_handler(state=AddCategory.AC1)
async def receive_name_of_category(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, item_type = data.get("msg_to_edit"), data.get("item_type")
    category_name, cat_id = message.text, random.randint(1111111, 9999999)
    await message.delete()
    await add_category(category_name, cat_id, item_type)
    await msg_to_edit.edit_caption("<b>Категория добавленна</b>", reply_markup=back_admin)
    await state.finish()


# ========================ADD SUBCATEGORY========================
# ASK FOR NAME OF SUBCATEGORY
@dp.callback_query_handler(text_startswith="adm_cat:", state=AddSubCategory.ASC1)
async def receive_category(call: CallbackQuery, state: FSMContext):
    category_name = call.data.split(":")[1]
    await state.update_data(category_name=category_name)
    msg_to_edit = await call.message.edit_caption("<b>Напишите название подкатегории</b>", reply_markup=back_admin)
    await AddSubCategory.next()
    await state.update_data(msg_to_edit=msg_to_edit)


# RECEIVE NAME OF THE SUBCATEGORY AND ADD IT
@dp.message_handler(state=AddSubCategory.ASC2)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, category_name, item_type = data.get("msg_to_edit"), data.get("category_name"), data.get("item_type")
    subcategory_name = message.text
    await message.delete()
    if item_type == "smm":
        sub_id = random.randint(1111111, 9999999)
        await add_subcategory(category_name, sub_id, subcategory_name)
        await msg_to_edit.edit_caption("<b>Под-категория добавленна</b>", reply_markup=back_admin)
        await state.finish()
    else:
        await msg_to_edit.edit_caption("<b>Напишите описание</b>", reply_markup=back_admin)
        await AddSubCategory.next()
        await state.update_data(sub_name=subcategory_name)


# RECEIVE NAME OF THE SUBCATEGORY AND ADD IT
@dp.message_handler(state=AddSubCategory.ASC3)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    desc = message.text
    await message.delete()
    await msg_to_edit.edit_caption("<b>Напишите цену за 1шт.</b>", reply_markup=back_admin)
    await AddSubCategory.next()
    await state.update_data(desc=desc)


# RECEIVE NAME OF THE SUBCATEGORY AND ADD IT
@dp.message_handler(state=AddSubCategory.ASC4)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    try:
        cost = int(message.text)
        await message.delete()
        await msg_to_edit.edit_caption("<b>Выберите тип товара</b>", reply_markup=product_type_menu)
        await AddSubCategory.next()
        await state.update_data(cost=cost)
    except ValueError:
        await msg_to_edit.edit_caption("<b> Неверное значение. Попробуйте еще раз</b>", reply_markup=back_admin)


# RECEIVE NAME OF THE SUBCATEGORY AND ADD IT
@dp.callback_query_handler(text_startswith="product_type:", state=AddSubCategory.ASC5)
async def receive_name_of_subcategory(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    desc, cat_id, sub_name = data.get("desc"), data.get("category_name"), data.get("sub_name")
    cost = data.get("cost")
    product_type = call.data.split(":")[1]
    sub_id = random.randint(1111111, 9999999)
    await add_product_subcategory(cat_id, sub_id, sub_name, desc, cost, product_type)
    await call.message.edit_caption("<b>Под-категория добавленна</b>", reply_markup=back_admin)
    await state.finish()


# ========================ADD ITEM========================
# RECEIVING CATEGORY NAME
@dp.callback_query_handler(text_startswith="adm_cat:", state=AddItem.AI1)
async def receive_category(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_type = data.get("item_type")
    category_name = call.data.split(":")[1]
    await state.update_data(category_name=category_name)
    await call.message.edit_caption("<b>Выберите подкатегорию, в которой будет находиться услуга:</b>",
                                    reply_markup=await admin_all_subcategories(category_name, item_type))
    await AddItem.next()


# RECEIVING SUBCATEGORY NAME
@dp.callback_query_handler(text_startswith="adm_sub:", state=AddItem.AI2)
async def receive_subcategory(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_type = data.get("item_type")
    subcategory_name = call.data.split(":")[1]
    if item_type == "product":
        subcategory = await select_product_subcategory(subcategory_name)
        text = "Отправьте файл" if subcategory[5] == "file" else "Отправьте текст товара"
    else:
        text = "<b>Напишите название услуги</b>"
    msg_to_edit = await call.message.edit_caption(text,
                                                  reply_markup=back_admin)

    await state.update_data(msg_to_edit=msg_to_edit, subcategory_name=subcategory_name)
    await AddItem.next()


# RECEIVE NAME OF THE ITEM
@dp.message_handler(state=AddItem.AI3, content_types=['text', 'document'])
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, subcategory_name = data.get("msg_to_edit"), data.get("subcategory_name")
    item_type = data.get("item_type")
    item_name = message.text
    await message.delete()
    if item_type == "product":
        subcategory = await select_product_subcategory(subcategory_name)
        product_id = random.randint(1000000, 9999999)
        if message.document:
            if subcategory[5] == "file":
                easy_chars, name = 'abcdefghijklnopqrstuvwxyz1234567890', ''
                for i in range(10):
                    name += random.choice(easy_chars)
                file = await message.document.download(f"items/{name}.{message.document.file_name.split('.')[-1]}")
                await add_product_item(subcategory[0], subcategory[1], file.name, product_id)
                await msg_to_edit.edit_caption("Товар добавлен",
                                               reply_markup=back_admin)
                await state.finish()
            else:
                await msg_to_edit.edit_caption("Вы пытаетесь добавить файл, хотя указали тип продажи 'текст'",
                                               reply_markup=back_admin)
        else:
            if subcategory[5] == "text":
                await add_product_item(subcategory[0], subcategory[1], message.text, product_id)
                await msg_to_edit.edit_caption("Товар добавлен",
                                               reply_markup=back_admin)
                await state.finish()
            else:
                await msg_to_edit.edit_caption("Вы пытаетесь добавить текст, хотя указали тип продажи 'файл'",
                                               reply_markup=back_admin)
        return

    await msg_to_edit.edit_caption("<b>Напишите описание услуги</b>\n"
                                   "<i>Вы можете использовать HTML разметку</i>", reply_markup=back_admin)
    await state.update_data(item_name=item_name)
    await AddItem.next()


# RECEIVE DESC OF THE ITEM
@dp.message_handler(state=AddItem.AI4)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    item_desc = message.text
    await message.delete()
    await msg_to_edit.edit_caption("<b>Напишите минимум и максимум для этой услуги через пробел. Пример:</b>\n"
                                   "100 1000", reply_markup=back_admin)
    await state.update_data(item_desc=item_desc)
    await AddItem.next()


# RECEIVE MIN AND MAX OF THE ITEM
@dp.message_handler(state=AddItem.AI5)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    min_max = message.text.split(" ")
    await message.delete()
    try:
        if len(min_max) == 2:
            if int(min_max[0]) > 0 and int(min_max[1]) > 0:
                await msg_to_edit.edit_caption(f"<b>Напишите цену за</b> <code>{min_max[0]}</code>",
                                               reply_markup=back_admin)
                await state.update_data(min_max=min_max)
                await AddItem.next()
            else:
                await msg_to_edit.edit_caption("<b>Значение не может быть меньше нуля, попробуйте еще раз</b>",
                                               reply_markup=back_admin)
        else:
            await msg_to_edit.edit_caption("<b>Не верное значение, попробуйте еще раз</b>", reply_markup=back_admin)
    except KeyError:
        await msg_to_edit.edit_caption("<b>Не верное значение, попробуйте еще раз</b>", reply_markup=back_admin)


# RECEIVE COST OF THE ITEM
@dp.message_handler(state=AddItem.AI6)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    cost = message.text
    await message.delete()
    try:
        if int(cost) > 0:
            await msg_to_edit.edit_caption("<b>Напишите ID сервиса</b>",
                                           reply_markup=back_admin)
            await state.update_data(cost=cost)
            await AddItem.next()
        else:
            await msg_to_edit.edit_caption("<b>Значение не может быть меньше нуля, попробуйте еще раз</b>",
                                           reply_markup=back_admin)
    except KeyError:
        await msg_to_edit.edit_caption("<b>Не верное значение, попробуйте еще раз</b>", reply_markup=back_admin)


# RECEIVE SERVICE ID AND ADD ITEM
@dp.message_handler(state=AddItem.AI7)
async def receive_name_of_subcategory(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, category_name, subcategory_name = data.get("msg_to_edit"), data.get("category_name"), data.get(
        "subcategory_name")
    item_name, item_desc, min_max = data.get("item_name"), data.get("item_desc"), data.get("min_max")
    cost = data.get("cost")
    service_id = message.text
    item_id = random.randint(1111111, 9999999)
    await add_item(
        item_name, subcategory_name, category_name, cost, min_max[0], min_max[1], service_id, item_desc, item_id
    )
    await message.delete()
    await msg_to_edit.edit_caption("<b>Услуга добавлена.</b>", reply_markup=back_admin)
    await state.finish()
