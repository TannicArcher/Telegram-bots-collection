import logging
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from create_bot import Bot, dp
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from database import sqlliteAdmin
import KeyBoards.KeyBoards as KB


class FSMCLogIn(StatesGroup):
    login = State()
    password = State()


async def question_log_in_admin(message: types.Message, state: FSMContext):
    flag = sqlliteAdmin.check_if_admin(message.from_user.id)
    print(flag == None)
    if flag:
        await message.answer("Вы вошли в панель админа", reply_markup=KB.admin_KeyBoard)
    else:
        await FSMCLogIn.login.set()
        await message.answer("Введите логин")


async def change_data_login(message: types.Message):
    await FSMCLogIn.login.set()
    await message.answer("Введите логин")


async def login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['login'] = message.text

    await FSMCLogIn.next()
    await message.answer("Введите пароль")


async def password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await sqlliteAdmin.add_admin(state)

    await message.answer("Вы успешно вошли", reply_markup=KB.admin_KeyBoard)

    await state.finish()


def register_handlers_client(dp: Dispatcher):

    dp.register_message_handler(question_log_in_admin, commands='admin')

    dp.register_message_handler(change_data_login, Text(equals="Изменить данные для входа", ignore_case=True))

    dp.register_message_handler(login, state=FSMCLogIn.login)
    dp.register_message_handler(password, state=FSMCLogIn.password)
