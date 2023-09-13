from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, Message

from filters import IsPrivate
from keyboards.inline.general_menu import *
from keyboards.reply.menu import main_menu_button
from loader import dp, bot
from states.states import SOSState
from utils.db_api.db_commands import *
from utils.other_utils import get_main_menu_pic


@dp.message_handler(commands=['show_id', 'id'])
async def bot_start(message: types.Message):
    await message.answer(f"ID чата: {message.chat.id}")


@dp.callback_query_handler(text="delete_this_message", state="*")
async def del_broadcast_msg(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(text="show_main_menu", state="*")
async def show_main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    photo, user = await get_main_menu_pic(), await select_user(call.from_user.id)
    await call.message.answer_photo(photo=photo,
                                    caption=f"<b>💳 Ваш баланс:</b> <code>{0 if not user else user[3]}</code> RUB",
                                    reply_markup=main_menu(call.from_user.id))


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    settings, photo, user = await select_settings(), await get_main_menu_pic(), await select_user(message.from_user.id)
    await message.answer("<b>🏡 Меню</b>", reply_markup=main_menu_button)
    await message.answer_photo(photo=photo,
                               caption=f"<b>💳 Ваш баланс:</b> <code>{0 if not user else user[3]}</code> RUB",
                               reply_markup=main_menu(message.from_user.id))
    if not user:
        ref_id = message.get_args()
        if ref_id:
            if ref_id != str(message.from_user.id):
                await add_user(message.from_user.id, ref_id)
                await bot.send_message(ref_id, f"<b><i>🎉У вас новый реферал! @{message.from_user.username}</i></b>")
        else:
            await add_user(message.from_user.id)
        await bot.send_message(settings[4], f"<b><i>🔔 Новый пользователь!\n👤Username: @{message.from_user.username}\n"
                                            f"🆔Telegram ID: {message.from_user.id}</i></b>")


@dp.message_handler(IsPrivate(), text="🏡 Меню", state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    photo, user = await get_main_menu_pic(), await select_user(message.from_user.id)
    await message.answer_photo(photo=photo, caption=f"<b>💳 Ваш баланс:</b> "
                                                    f"<code>{0 if not user else user[3]}</code> RUB",
                               reply_markup=main_menu(message.from_user.id))


@dp.callback_query_handler(text="back_to_main_menu", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user = await select_user(call.from_user.id)
    await call.message.edit_caption(f"💳 Ваш баланс: <code>{0 if not user else user[3]}</code> RUB",
                                    reply_markup=main_menu(call.from_user.id))


@dp.callback_query_handler(text="info")
async def info(call: CallbackQuery):
    await call.message.edit_caption("<b>🔥 Наш бот продает Множество товаров и услуг также автоматическая накрутка\n\n"
                                    "⭐️ Всегда качественный товар\n"
                                    "⭐️ Лучшие цены на накрутку \n"
                                    "⭐️ Поддержка работает больше 12 часов в день\n"
                                    "⭐️ Множество товаров и услуг \n"
                                    "⭐️ Замена товара в случае невалида \n\n"
                                    "🎉 Покупая у нас ты становишься лучшим!</b>",
                                    reply_markup=back_to_main_menu)


@dp.callback_query_handler(text="affiliate")
async def info(call: CallbackQuery):
    refs, bot_info, user = await select_all_refs(call.from_user.id), await bot.get_me(), await select_user(
        call.from_user.id)
    await call.message.edit_caption(f"<b><i>🤝 Партнёрская программа\n\n"
                                    f"🔗 Ссылка: \n"
                                    f"<code>https://t.me/{bot_info.username}?start={call.from_user.id}</code>\n\n👥"
                                    f" Рефералов: {len(refs)}\n🌀 Процент: 10%\n"
                                    f"💸 Всего заработано: {user[5]}₽\n\n"
                                    f"🔥Если вы пригласите человека который пополнит баланс в боте,"
                                    f" вам дадут 10% от пополнения вам на баланс!</i></b>",
                                    reply_markup=back_to_main_menu)


@dp.callback_query_handler(text="order_history")
async def show_info(call: CallbackQuery):
    await call.message.edit_caption(f"<b>🛒 Выберите какую историю заказов вы хотите посмотреть:</b>",
                                    reply_markup=order_history_menu)


@dp.callback_query_handler(text_startswith="history:")
async def show_info(call: CallbackQuery):
    order_type = call.data.split(":")[1]
    orders = await select_user_orders(call.from_user.id, order_type)
    await call.message.edit_caption(f"🔖 Последние 10 созданных заказов:",
                                    reply_markup=back_to_main_menu)
    for i in range(len(orders) - 1, len(orders) - 11, -1):
        try:
            if i < 0:
                break
            if order_type == "smm":
                await call.message.answer(f"🛒 Созданный заказ:\n"
                                          f"🔗Ссылка: {orders[i][3]}\n"
                                          f"📊Количество: {orders[i][2]}\n"
                                          f"📦Услуга: {orders[i][1]}\n"
                                          f"🆔ID Заказа: {orders[i][4]}\n"
                                          f"💳Списанная сумма: {orders[i][5]}")
            else:
                await call.message.answer(f"🛒 Созданный заказ:\n"
                                          f"📦Товар: {orders[i][1]}\n"
                                          f"📊Количество: {orders[i][2]}\n"
                                          f"💳Списанная сумма: {orders[i][5]}")
        except IndexError:
            break


@dp.callback_query_handler(text="sos")
async def sos_message(call: CallbackQuery):
    await call.message.edit_caption("<b>🆘 Если у вас случилась проблему обратись в нашу тех поддержку:</b>",
                                    reply_markup=sos_menu)


@dp.callback_query_handler(text_startswith="sos:")
async def sos_message(call: CallbackQuery, state: FSMContext):
    mail_type = call.data.split(":")[1]
    mail = await select_mail(call.from_user.id)
    if not mail:
        await call.message.edit_caption("❓Введите ваш вопрос, писать понятно или же не получите ответа:",
                                        reply_markup=back_to_main_menu)
        await SOSState.SS1.set()
        await state.update_data(message_to_edit=call.message, mail_type=mail_type)
    else:
        await call.answer("❗️У вас уже есть отправленное сообщение. Пожалуйста дождитесь его обработки",
                          show_alert=True)


@dp.message_handler(state=SOSState.SS1)
async def receive_msg(message: Message, state: FSMContext):
    msg, data = message.text, await state.get_data()
    msg_to_edit, mail_type = data.get("message_to_edit"), data.get("mail_type")
    await message.delete()
    await add_mail(message.from_user.id, mail_type, message.text)
    await msg_to_edit.edit_caption("✅ Запрос отправлен\n"
                                   "🧭Среднее время ответа: 2-4 часа", reply_markup=back_to_main_menu)
    await state.finish()
