from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.personal_acc_menu import *
from loader import dp, bot
from states.states import ShowOrderStatusState, PromoStates
from utils.db_api.db_commands import select_user, select_user_orders, update_bal, select_settings
from utils.nakrytka_api import order_status


@dp.callback_query_handler(text="personal_acc")
async def personal_acc(call: CallbackQuery):
    user = await select_user(call.from_user.id)
    await call.message.edit_caption(f"🖥<b>Личный кабинет:</b>\n"
                                    f"🆔<i><b>Мой ID:</b></i> <code>{call.from_user.id}</code>\n"
                                    f"<i><b>🛍Всего покупок:</b></i>  <code>{user[1]}</code>\n"
                                    f"<i><b>📥Всего пополнено:</b></i> <code>{user[2]}</code>\n"
                                    f"<i><b>💵Баланс:</b></i>  <code>{user[3]}</code>", reply_markup=personal_menu)


@dp.callback_query_handler(text="personal_acc", state="*")
async def personal_acc(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await select_user(call.from_user.id)
    await call.message.edit_caption(f"🖥<b>Личный кабинет:</b>\n"
                                    f"🆔<i><b>Мой ID:</b></i> <code>{call.from_user.id}</code>\n"
                                    f"<i><b>🛍Всего покупок:</b></i>  <code>{user[1]}</code>\n"
                                    f"<i><b>📥Всего пополнено:</b></i> <code>{user[2]}</code>\n"
                                    f"<i><b>💵Баланс:</b></i>  <code>{user[3]}</code>", reply_markup=personal_menu)


@dp.callback_query_handler(text="my_orders")
async def show_my_orders(call: CallbackQuery):
    orders = await select_user_orders(call.from_user.id)
    text = ""
    for order in orders:
        text += f"<code>{order[4]}</code> <b>|</b> <code>{order[1]}</code> " \
                f"<b>|</b> <code>{order[2]}</code> <b>|</b> <code>{order[3]}</code>\n"
    if text == "":
        await call.message.edit_caption("<b>У вас пока нет заказов.</b>", reply_markup=my_orders_menu)
    else:
        await call.message.edit_caption(f"<b>ID Заказа | Категория | Количество | URL</b>\n{text}",
                                        reply_markup=my_orders_menu)


@dp.callback_query_handler(text="show_order_status")
async def show_order_status(call: CallbackQuery, state: FSMContext):
    await ShowOrderStatusState.SO1.set()
    await state.update_data(msg_to_edit=call.message)
    await call.message.edit_caption("<b>Напишите номер вашего заказа</b>")


@dp.message_handler(state=ShowOrderStatusState.SO1)
async def show_order_status(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    order = order_status(message.text)
    await message.delete()
    if order.get("error"):
        await msg_to_edit.edit_caption(f"<b>Заказа с данным ID не существует</b>\nПопробуйте еще раз.",
                                       parse_mode="HTML", reply_markup=my_orders_menu)
    else:
        status = "В процессе" if order['status'] == "Pending" else "Выполнен"
        await msg_to_edit.edit_caption(f"<b>ID заказа:</b> <code>{message.text}</code>\n"
                                       f"<b>Статус заказа:</b> <code>{status}</code>\n"
                                       f"<b>Осталось:</b> <code>{order['remains']}</code>",
                                       reply_markup=my_orders_menu)
        await state.finish()


@dp.callback_query_handler(text="promo")
async def get_promo(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_caption("<b>Введите промокод</b>", reply_markup=my_orders_menu)
    await PromoStates.P1.set()
    await state.update_data(msg_to_edit=msg_to_edit)


@dp.message_handler(state=PromoStates.P1)
async def receive_promo(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    promo, settings = await select_promo(message.text), await select_settings()
    await message.delete()
    if promo:
        await add_activated_promo_count()
        await add_activated_promo_money(promo[1])
        await update_bal(message.from_user.id, promo[1])
        await del_promo(message.text)
        await msg_to_edit.edit_caption(f"<b>🔰Промокод активирован\nВы получили {promo[1]} руб на баланс</b>",
                                       reply_markup=my_orders_menu)
        await bot.send_message(settings[6], f"<b>🔰 Активирован промокод</b>\n\n"
                                            f"<i>◽️Пользователь:  @{message.from_user.username}\n"
                                            f"◽️Айди человека:  {message.from_user.id}\n"
                                            f"◽️Сумма: {promo[1]}\n"
                                            f"◽️Промокод: {promo[0]}</i>")
    else:
        await msg_to_edit.edit_caption(f"<b>Такого промокода не существует, попробуйте еще раз</b>",
                                       reply_markup=my_orders_menu)
