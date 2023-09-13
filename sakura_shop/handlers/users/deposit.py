from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.general_menu import back_to_main_menu
from keyboards.inline.deposit_menu import check_menu, payment_methods_menu
from loader import dp, bot
from states.states import BalanceState
from utils.db_api.db_commands import update_bal, select_user, \
    update_full_added_bal, update_ref_bal, select_settings
from utils.qiwi import balance, check_payment, check_payment_p2p


@dp.callback_query_handler(text_startswith="deposit")
async def add_balance_main(call: CallbackQuery, state: FSMContext):
    msg_to_edt = await call.message.edit_caption("<b>👉🏻Введите необходимую сумму для пополнения:</b>",
                                                 reply_markup=back_to_main_menu)
    await BalanceState.BS1.set()
    await state.update_data(msg_to_edt=msg_to_edt)


@dp.message_handler(state=BalanceState.BS1)
async def add_balance_2(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edt = data.get("msg_to_edt")
    balance_to_add = message.text
    await message.delete()
    try:
        if int(balance_to_add) >= 1:
            await msg_to_edt.edit_caption("💳 <b>Выберете платёжную систему для депозита:</b>",
                                          reply_markup=payment_methods_menu)
            await state.update_data(balance_to_add=balance_to_add)
            await BalanceState.next()
        else:
            await message.answer("Не верное количество, попробуйте еще раз")
    except ValueError:
        await message.answer("Не верное количество, попробуйте еще раз")


@dp.callback_query_handler(state=BalanceState.BS2, text_startswith="payment_method:")
async def add_balance_2(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_to_edt, balance_to_add = data.get("msg_to_edt"), data.get("balance_to_add")
    method = call.data.split(":")[1]
    settings = await select_settings()
    keyboard, bill_id, url = await check_menu(balance_to_add, call.from_user.id, method,
                                              datetime.now() + timedelta(minutes=10))
    text = f"<b>🔥 Для пополнения баланса в данном боте вам необходимо перевести на указанные реквизиты:\n\n" \
           f"📱Номер: <code>+{settings[0]}</code>\n" \
           f"🗯Комментарий: <code>{call.from_user.id}</code>\n" \
           f"💰Сумма: <code>{balance_to_add}</code>\n\n" \
           f"⛔️Перевод без комментария не будет зачислен на баланс бота!</b>"
    if method != "num":
        text = "🔥<b>Для пополнения с помощью платёжной системы (P2P Qiwi bank)</b>\n\n" \
               "❕<i>Просто перейдите по ссылке ниже и оплатите.\n" \
               "❕Если вам нужно пополнить с помощью карты нажмите «Банковской картой»\n" \
               "❕Не больше 5000₽ (пишите админу при большых пополнений)</i>\n\n" \
               "<b>⭐️Нажмите на кнопку ниже и оплатите⭐️</b>"
    post_text = f"🔗Ссылка: <a href='{url}'>(Кликабельно)</a>" if method != "num" else \
        f"◾️Номер: {settings[0]}\n" \
        f"◾️Комментарий: {call.from_user.id}"
    await msg_to_edt.edit_caption(text,
                                  reply_markup=keyboard)
    past_bal = await balance()
    await state.update_data(method=method, balance_to_add=balance_to_add, bill_id=bill_id, past_bal=past_bal)
    await BalanceState.next()


@dp.callback_query_handler(text="check", state=BalanceState.BS3)
async def add_balance_main(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bill_id, method, balance_to_add = data.get("bill_id"), data.get("method"), data.get("balance_to_add")
    past_bal = data.get("past_bal")
    settings = await select_settings()
    with open("main_menu.jpg", "rb") as file:
        photo = file.read()
    if method == "num":
        if await check_payment(call.from_user.id, balance_to_add, past_bal):
            user = await select_user(call.from_user.id)
            bal_to_add = int(balance_to_add) + user[6]
            await update_bal(call.from_user.id, bal_to_add)
            await update_full_added_bal(call.from_user.id, bal_to_add)
            if user[6]:
                await update_bal(user[6], round(bal_to_add / 10))
                await update_ref_bal(user[6], round(bal_to_add / 10))
            await call.message.delete()
            await call.message.answer_photo(photo=photo, caption="<b>Готово, платеж получен, баланс начислен ✅</b>",
                                            reply_markup=back_to_main_menu)
            user = await select_user(call.from_user.id)
            await bot.send_message(settings[4], f"""<b>
🤑 Сделан новый депозит

<i>◽️Пользователь: @{call.from_user.username}
◽️Айди человека: {call.from_user.id}
◽️Сумма: {bal_to_add}
◽️Новый баланс: {user[3]}</i></b>""")
            await state.finish()
        else:
            await call.message.answer("Я еще не получил оплаты")
    else:
        if await check_payment_p2p(bill_id):
            user = await select_user(call.from_user.id)
            bal_to_add = int(balance_to_add) + user[6]
            await update_bal(call.from_user.id, bal_to_add)
            await update_full_added_bal(call.from_user.id, bal_to_add)
            if user[6]:
                await update_bal(user[6], round(bal_to_add / 10))
                await update_ref_bal(user[6], round(bal_to_add / 10))
            await call.message.delete()
            await call.message.answer_photo(photo=photo, caption="<b>Готово, платеж получен, баланс начислен ✅</b>",
                                            reply_markup=back_to_main_menu)
            user = await select_user(call.from_user.id)
            await bot.send_message(settings[4], f"""<b>
🤑 Сделан новый депозит </b>

<i>◽️Пользователь: @{call.from_user.username}
◽️Айди человека: {call.from_user.id}
◽️Сумма: {bal_to_add}
◽️Новый баланс: {user[3]}</i>""")
            await state.finish()
        else:
            await call.message.answer("Я еще не получил оплаты")
