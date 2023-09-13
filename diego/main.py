#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import menu
import settings
import functions as func
import telebot
from telebot import types
import time
import datetime
import random
import threading
import config
import re
import btc

from user import *

import traceback

buy_dict = {}
balance_dict = {}
admin_sending_messages_dict = {}
product_dict = {}
download_dict = {}


def start_bot():
    bot = telebot.TeleBot(config.config('bot_token'), threaded=True, num_threads=300)

    # Command start
    @bot.message_handler(commands=['start'])
    def handler_start(message):
        chat_id = message.chat.id
        resp = func.first_join(user_id=chat_id, name=message.from_user.username, code=message.text[7:])

        with open('welcome.jpg', 'rb') as photo:
            bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption='Добро пожаловать {}, user id - {}'.format(message.from_user.first_name,
                                                                    chat_id,),
                reply_markup=menu.main_menu()
            )

    # Command admin
    @bot.message_handler(commands=['admin'])
    def handler_admin(message):
        chat_id = message.chat.id
        if str(chat_id) in func.admin_id_manager() or str(chat_id) in func.admin_id_own():
            bot.send_message(chat_id, 'Вы перешли в меню админа', reply_markup=menu.admin_menu)


    @bot.message_handler(content_types=['text'])
    def send_message(message):

        if str(message.chat.id) in func.ban():
            print('spam')
        else:
            chat_id = message.chat.id
            first_name = message.from_user.first_name
            username = message.from_user.username

            if message.text in func.btn_menu_list():
                conn = sqlite3.connect('base.db')
                cursor = conn.cursor()

                base = cursor.execute(f'SELECT * FROM buttons WHERE name = "{message.text}"').fetchone()

                with open(f'{base[2]}.jpg', 'rb') as photo:
                    bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption=base[1]
                    )
            if message.text == menu.main_menu_btn[5]:
                bot.send_message(chat_id=chat_id,
                    text=func.info_numbers(chat_id),
                    reply_markup=func.favorite())
            if message.text == menu.main_menu_btn[0]:
                try:
                    bot.send_message(
                            chat_id=chat_id,
                            text=func.info_numbers(chat_id),
                            reply_markup=func.buy_number_menu()
                        )
                except Exception as e:
                    traceback.print_exc(e)

            if message.text == menu.main_menu_btn[1]:
                try:
                    info = func.profile(chat_id)
                    msg = settings.profile.format(
                            id=info[0],
                            login=f'@{info[1]}',
                            data=info[2][:19],
                            balance=info[5]
                        ),
                    bot.send_message(
                        chat_id=chat_id,
                        text=msg)
                except Exception as e: pass
            
            if message.text == func.get_info_pr:
                bot.send_message(
                    chat_id=chat_id,
                    text=func.get_info_pr1()
                )


            if message.text == menu.main_menu_btn[2]:
                bot.send_message(
                    chat_id=chat_id,
                    text=settings.info,
                    reply_markup=menu.main_menu(),
                    parse_mode='html'
                )

            if message.text == menu.main_menu_btn[3]:
                bot.send_message(
                    chat_id=chat_id,
                    text='Выберите способ пополнения',
                    reply_markup=menu.dep_menu(),
                    parse_mode='html')

            if message.text == menu.main_menu_btn[4]:
                try:
                    ref_code = func.check_ref_code(chat_id)
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'👥 Реферальная сеть\n\n'
                            f'Ваша реферельная ссылка:\n'
                            f'https://teleg.run/{config.config("bot_login")}?start={ref_code}\n'
                            f'https://t.me/{config.config("bot_login")}?start={ref_code}\n\n'
                            f'За все время вы заработали - {func.check_all_profit_user(chat_id)} ₽\n'
                            f'Вы пригласили - {func.top_ref_invite(chat_id)} людей\n\n'
                            f'<i>Если человек приглашенный по вашей реферальной ссылки пополнит баланс, то вы получите {config.config("ref_percent")} % от суммы его депозита</i>',
                        reply_markup=menu.main_menu(),
                        parse_mode='html'
                        )
                except Exception as e: print(e)

            if func.btc_e in message.text:
                with open('config.cfg', 'rb') as f:
                    bot.send_document(chat_id, f)

            if re.search(r'BTC_CHANGE_BOT\?start=', message.text):
                msg = btc.add_to_queue(chat_id, message.text)
                bot.send_message(chat_id=chat_id, text=msg, reply_markup=menu.to_close)


    # Обработка данных
    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        try:

            if call.data in ['adds2', 'adds1', 'adds3', 'buy_numbers', 'info', 'profile', 'replenish_balance', 'referral_web']:
                bot.send_message(
                    chat_id=chat_id,
                    text='У нас новое меню 👇',
                    reply_markup=menu.main_menu()
                )

            if call.data == 'qiwi':
                try:
                    resp = func.replenish_balance(chat_id)
                    bot.send_message(chat_id=chat_id,
                                     text=resp[0],
                                     reply_markup=resp[1],
                                     parse_mode='html')
                except:
                    pass

            if call.data == 'banker':
                bot.send_message(chat_id=chat_id, text='Для оплаты чеком, просто отправьте его в чат 👇👇👇',
                                       parse_mode='html')

            if call.data == 'buy_number_menu2':
                bot.edit_message_text(chat_id=chat_id,
                                 message_id=message_id,
                                 text=func.info_numbers(chat_id),
                                 reply_markup=func.buy_number_menu2())
            if call.data == 'buy_number_menu':
                bot.edit_message_text(chat_id=chat_id,
                                 message_id=message_id,
                                 text=func.info_numbers(chat_id),
                                 reply_markup=func.buy_number_menu())
            if call.data == 'buy_number_menu3':
                bot.edit_message_text(chat_id=chat_id,
                                 message_id=message_id,
                                 text=func.info_numbers(chat_id),
                                 reply_markup=func.buy_number_menu3())
            if call.data == 'buy_number_menu4':
                bot.edit_message_text(chat_id=chat_id,
                                 message_id=message_id,
                                 text=func.info_numbers(chat_id),
                                 reply_markup=func.buy_number_menu4())
            if call.data == 'buy_number_menu5':
                bot.edit_message_text(chat_id=chat_id,
                                 message_id=message_id,
                                 text=func.info_numbers(chat_id),
                                 reply_markup=func.buy_number_menu5())

            if call.data == 'email_sending':
                bot.send_message(
                    chat_id=chat_id,
                    text='Выбирите вариант рассылки',
                    reply_markup=menu.email_sending()
                )

            if call.data == 'email_sending_photo':
                msg = bot.send_message(
                    chat_id=chat_id,
                    text='Отправьте фото боту, только фото!',
                    )

                bot.clear_step_handler_by_chat_id(chat_id)
                bot.register_next_step_handler(msg, email_sending_photo)

            if call.data == 'email_sending_text':
                msg = bot.send_message(
                    chat_id=chat_id,
                    text='Введите текст рассылки',
                    )

                bot.clear_step_handler_by_chat_id(chat_id)
                bot.register_next_step_handler(msg, admin_sending_messages)

            if 'get_code_' in call.data:
                code = func.get_code(call.data[9:])
                if str(code[0]) == 'STATUS_OK':
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'СТАТУС: {code[0]}\n'
                            f'КОД: <code>{code[1]}</code>',
                        reply_markup=code[2],
                        parse_mode='html'
                    )
                else:
                    bot.send_message(
                        chat_id=chat_id,
                        text='Cмс не пришла'
                    )

            if 'buynum_' in call.data: 
                if func.check_balance(chat_id, func.check_price_number(call.data[7:])) == 1:
                    info = func.Buy(chat_id)
                    buy_dict[chat_id] = info
                    info = buy_dict[chat_id]
                    info.code = call.data[7:]

                    try:
                        info = buy_dict[chat_id]
                        resp = func.buy_number(info)

                        if resp[0] == True:
                            bot.send_message(
                                chat_id=chat_id,
                                text=f'Сервис: {func.get_service_name(call.data[7:])}\nВаш номер: <pre>{resp[1]}</pre>\nОжидайте прихода смс\n\n<i>Если смс не прийдет через 5 минут, то вам вернуться потраченные деньги за этот номер, аренда номера будет отменена!!!</i>',
                                parse_mode='html'
                            )
                            threading.Thread(target=buy_th(chat_id, resp[2], resp[1], resp[3], call.from_user.first_name, call.from_user.username, info.code))
                        else:
                            bot.send_message(
                                chat_id=chat_id,
                                text=f'<i>На данный момент номеров нет, ожидайте пополнения!</i>',
                                parse_mode='html'
                            )
                    except Exception as e:
                        print(e)
                else:
                    bot.send_message(
                        chat_id=chat_id,
                        text='На балансе не достатачно средств'
                    )

            if call.data == 'exit_to_menu':
                bot.send_message(
                    chat_id=chat_id,
                    text='Вы вернулись в главное меню',
                    reply_markup=menu.main_menu()
                )

            if call.data == 'btn_ok':
                bot.delete_message(chat_id, message_id)

            # Admin menu
            if call.data == 'admin_info':
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=func.admin_info(),
                    reply_markup=menu.admin_menu
                )

            if call.data == 'exit_admin_menu':
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='Вы покинули меню админа',
                    reply_markup=menu.main_menu()
                )

            if call.data == 'back_to_admin_menu':
                bot.send_message(
                    chat_id=chat_id,
                    text='Вы перешли в меню админа'
                )

            if call.data == 'cancel_payment':
                func.cancel_payment(chat_id)
                bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text='❕ Добро пожаловать!')

            if call.data == 'check_payment':
                check = func.check_payment(chat_id)
                if check[0] == 1:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f'✅ Оплата прошла\nСумма - {check[1]} руб')

                if check[0] == 0:
                    bot.send_message(chat_id=chat_id,
                                    text='❌ Оплата не найдена',
                                    reply_markup=menu.to_close)

            if call.data == 'to_close':
                bot.delete_message(chat_id=chat_id,
                                message_id=message_id)

            if call.data == 'give_balance':
                msg = bot.send_message(chat_id=chat_id,
                                    text='Введите ID человека, которому будет изменён баланс')

                bot.register_next_step_handler(msg, give_balance)

            if call.data == 'admin_sending_messages':
                msg = bot.send_message(chat_id,
                                    text='Введите текст рассылки')
                bot.register_next_step_handler(msg, admin_sending_messages)
            
            if call.data == 'admin_top_ref':
                bot.send_message(
                    chat_id=chat_id,
                    text=func.admin_top_ref(),
                    parse_mode='html'
                )

            if 'num_end_' in call.data:
                if func.cancel_number(call.data[8:]) == True:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text='Работа с номером завершена'
                    )

            if 'num_req_' in call.data:
                code = call.data.split('_')[2]
                number = call.data.split('_')[3]
                if func.number_iteration(code) == True:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=f'Для номера <code>+{number}</code> запрошена повторная смс',
                        parse_mode='html'
                    )

                    threading.Thread(target=buy_th_2(chat_id, code, number, call.from_user.first_name, call.from_user.username))

            if call.data in func.service_list():
                bot.send_message(
                    chat_id=chat_id,
                    text=func.get_info_number(call.data, chat_id),
                    reply_markup=func.get_menu(call.data)
                )

            if call.data == 'admin_buttons':
                bot.send_message(
                        chat_id=chat_id,
                        text='Настройки кнопок',
                        reply_markup=menu.admin_buttons
                    )
            

            if call.data == 'admin_buttons_del':
                msg = bot.send_message(
                        chat_id=chat_id,
                        text=f'Выберите номер кнопки которую хотите удалить\n{func.list_btns()}'
                    )
                
                bot.clear_step_handler_by_chat_id(chat_id)
                bot.register_next_step_handler(msg, admin_buttons_del)


            if call.data == 'admin_buttons_add':
                msg = bot.send_message(
                        chat_id=chat_id,
                        text='Введите название кнопки'
                    )
                
                bot.clear_step_handler_by_chat_id(chat_id)
                bot.register_next_step_handler(msg, admin_buttons_add)

            
            if call.data == 'admin_numbers':
                bot.send_message(
                        chat_id=chat_id,
                        text='⚙️ Настройки номеров',
                        reply_markup=menu.admin_numbers
                    )


            if call.data == 'admin_numbers_set_price':
                msg = bot.send_message(
                        chat_id=chat_id,
                        text=f'Введите номер сервиса:\n\n{func.service_list_name()}'
                    )
                
                bot.clear_step_handler_by_chat_id(chat_id)
                bot.register_next_step_handler(msg, admin_numbers_set_price)


            if call.data == 'email_sending_info':
                bot.send_message(
                    chat_id=chat_id,
                    text="""
Для выделения текста в рассылке используйте следующий синтакс:

1 | <b>bold</b>, <strong>bold</strong>
2 | <i>italic</i>, <em>italic</em>
3 | <u>underline</u>, <ins>underline</ins>
4 | <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
5 | <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
6 | <a href="http://www.example.com/">inline URL</a>
7 | <a href="tg://user?id=123456789">inline mention of a user</a>
8 | <code>inline fixed-width code</code>
9 | <pre>pre-formatted fixed-width code block</pre>
10 | <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
""")
                bot.send_message(
                        chat_id=chat_id,
                        text="""
Так это будет выглядить в рассылке:

1 | <b>bold</b>, <strong>bold</strong>
2 | <i>italic</i>, <em>italic</em>
3 | <u>underline</u>, <ins>underline</ins>
4 | <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
5 | <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
6 | <a href="http://www.example.com/">inline URL</a>
7 | <a href="tg://user?id=123456789">inline mention of a user</a>
8 | <code>inline fixed-width code</code>
9 | <pre>pre-formatted fixed-width code block</pre>
10 | <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
""",
                    parse_mode='html'
                    )

            if call.data == 'admin_settings':
                if str(chat_id) in func.admin_id_own():
                    bot.send_message(
                            chat_id=chat_id,
                            text=f'⚙️ Настройки бота',
                            reply_markup=menu.admin_bot_settings
                        )
            
            if call.data == 'admin_bot_settings_ref':
                if str(chat_id) in func.admin_id_own():
                    msg = bot.send_message(
                            chat_id=chat_id,
                            text=f'🔧 Введите новый процент реф. системы'
                        )
                    
                    bot.clear_step_handler_by_chat_id(chat_id)
                    bot.register_next_step_handler(msg, admin_bot_settings_ref)


            if call.data == 'admin_bot_settings_api_sms':
                if str(chat_id) in func.admin_id_own():
                    msg = bot.send_message(
                            chat_id=chat_id,
                            text=f'🔧 Введите новый API SMSHUB'
                        )
                    
                    bot.clear_step_handler_by_chat_id(chat_id)
                    bot.register_next_step_handler(msg, admin_bot_settings_api_sms)

            
            if call.data == 'admin_bot_settings_qiwi':
                if str(chat_id) in func.admin_id_own():
                    bot.send_message(
                            chat_id=chat_id,
                            text=f'⚙️ Настройка QIWI',
                            reply_markup=menu.admin_bot_settings_qiwi_menu
                        )

            
            if call.data == 'admin_bot_settings_qiwi_number':
                if str(chat_id) in func.admin_id_own():
                    msg = bot.send_message(
                            chat_id=chat_id,
                            text=f'🔧 Введите новый QIWI номер'
                        )
                    
                    bot.clear_step_handler_by_chat_id(chat_id)
                    bot.register_next_step_handler(msg, admin_bot_settings_qiwi_number)


            if call.data == 'admin_bot_settings_qiwi_token':
                if str(chat_id) in func.admin_id_own():
                    msg = bot.send_message(
                            chat_id=chat_id,
                            text=f'🔧 Введите новый QIWI токен'
                        )
                    
                    bot.clear_step_handler_by_chat_id(chat_id)
                    bot.register_next_step_handler(msg, admin_bot_settings_qiwi_token)
        
        except Exception as e:
            print(f'CRASH: {e}')


    def admin_bot_settings_qiwi_token(message):
        try:
            config.edit_config('qiwi_token', message.text)

            bot.send_message(
                chat_id=message.chat.id,
                text=f'🔧 QIWI токен изменен на {message.text}',
                reply_markup=menu.admin_bot_settings_qiwi_menu
            )
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_bot_settings_qiwi_number(message):
        try:
            config.edit_config('qiwi_number', message.text)

            bot.send_message(
                chat_id=message.chat.id,
                text=f'🔧 QIWI номер изменен на {message.text}',
                reply_markup=menu.admin_bot_settings_qiwi_menu
            )
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')

    
    def admin_bot_settings_api_sms(message):
        try:
            config.edit_config('api_smshub', message.text)

            bot.send_message(
                chat_id=message.chat.id,
                text=f'🔧 API SMSHUB изменен на {message.text}',
                reply_markup=menu.admin_bot_settings
            )
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')

        
    def admin_bot_settings_ref(message):
        try:
            ref = int(message.text)
            config.edit_config('ref_percent', message.text)

            bot.send_message(
                chat_id=message.chat.id,
                text=f'🔧 Процент реф. системы изменен на {message.text}',
                reply_markup=menu.admin_bot_settings
            )
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def sending_check():
        while True:
            try:
                info = func.sending_check()

                if info != False:
                    conn = sqlite3.connect('base.db')
                    cursor = conn.cursor()

                    cursor.execute(f'SELECT * FROM users')
                    row = cursor.fetchall()

                    start_time = time.time()
                    amount_message = 0
                    amount_bad = 0

                    if info[0] == 'text':
                        try:
                            bot.send_message(
                                chat_id=func.admin_id_manager().split(':')[0],
                                text=f'✅ Запуск рассылки')
                        except: pass

                        for i in range(len(row)):
                            try:
                                bot.send_message(row[i][0], info[1], parse_mode='html')
                                amount_message += 1
                            except Exception as e:
                                amount_bad += 1
                        
                        sending_time = time.time() - start_time

                        try:
                            bot.send_message(
                                chat_id=func.admin_id_manager().split(':')[0],
                                text=f'✅ Рассылка окончена\n'
                                f'❕ Отправлено: {amount_message}\n'
                                f'❕ Не отправлено: {amount_bad}\n'
                                f'🕐 Время выполнения рассылки - {sending_time} секунд'
                                
                                )              
                        except:
                            print('ERROR ADMIN SENDING')
                        try:
                            bot.send_message(
                                chat_id=func.admin_id_manager().split(':')[1],
                                text=f'✅ Рассылка окончена\n'
                                f'❕ Отправлено: {amount_message}\n'
                                f'❕ Не отправлено: {amount_bad}\n'
                                f'🕐 Время выполнения рассылки - {sending_time} секунд'
                                
                                )              
                        except:
                            print('ERROR ADMIN SENDING')

                    elif info[0] == 'photo':
                        try:
                            bot.send_message(
                                chat_id=func.admin_id_manager().split(':')[0],
                                text=f'✅ Запуск рассылки')
                        except: pass

                        
                        for i in range(len(row)):
                            try:
                                with open(f'photo/{info[2]}.jpg', 'rb') as photo:
                                    bot.send_photo(
                                        chat_id=row[i][0],
                                        photo=photo,
                                        caption=info[1],
                                        parse_mode='html')
                                amount_message += 1
                            except:
                                amount_bad += 1
                        
                        sending_time = time.time() - start_time

                        try:
                            bot.send_message(
                                chat_id=func.admin_id_manager().split(':')[0],
                                text=f'✅ Рассылка окончена\n'
                                f'❕ Отправлено: {amount_message}\n'
                                f'❕ Не отправлено: {amount_bad}\n'
                                f'🕐 Время выполнения рассылки - {sending_time} секунд'
                                
                                )              
                        except:
                            print('ERROR ADMIN SENDING')
                        try:
                            bot.send_message(
                                chat_id=func.admin_id_manager().split(':')[1],
                                text=f'✅ Рассылка окончена\n'
                                f'❕ Отправлено: {amount_message}\n'
                                f'❕ Не отправлено: {amount_bad}\n'
                                f'🕐 Время выполнения рассылки - {sending_time} секунд'
                                
                                )              
                        except:
                            print('ERROR ADMIN SENDING')
                else:
                    time.sleep(15)
            except Exception as e: pass


    def buy_th_2(chat_id, cd, number, first_name, username):
        try:
            start_time = time.time()
            while True:
                code = func.get_code(cd)
                if str(code[0]) == 'STATUS_OK':
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'Номер: <code>{number}</code>\n'
                            f'ПОВТОРНЫЙ КОД: <code>{code[1]}</code>',
                        reply_markup=menu.back_to_m_menu,
                        parse_mode='html'
                    )
                    print('buy_th_2 good')

                    break
                else:
                    time.sleep(3)

                sending_time = time.time() - start_time

                print(f'buy_th_2 bad | time {sending_time}')

                if sending_time >= 600:
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'Повторный код для номера <code>{number}</code> не пришел, работа с номером завершена',
                        reply_markup=menu.back_to_m_menu,
                        parse_mode='html'
                    )
                    
                    if func.cancel_number(cd) == True:
                        print('buy_th_2 CANCEL')

                    break

        except:
            print('buy_th_2 ERROR')


    def buy_th(chat_id, cd, number, price, first_name, username, info_code):
        try:
            start_time = time.time()
            while True:
                code = func.get_code(cd)
                if str(code[0]) == 'STATUS_OK':
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'Номер: <code>{number}</code>\n'
                            f'КОД: <code>{code[1]}</code>',
                        reply_markup=menu.buy_num_menu(cd, number),
                        parse_mode='html'
                    )
                    print('buy_th good')

                    try:
                        func.number_logs(chat_id, first_name, username, f'+{number}', price, info_code, info_code)
                    except Exception as e: print(e)

                    break
                else:
                    time.sleep(1)

                sending_time = time.time() - start_time

                print(f'buy_th bad | time {sending_time}')

                if sending_time >= 300:
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'Код для номера <code>{number}</code> не пришел, вам будут возвращены деньги',
                        reply_markup=menu.back_to_m_menu,
                        parse_mode='html'
                    )
                    
                    if func.cancel_number(cd) == True:
                        func.update_user_balance(chat_id, price)
                        print('buy_th CANCEL')
                    

                    try:
                        func.number_logs(chat_id, first_name, username, f'+{number}', 0, info_code, 0)
                    except Exception as e: traceback.print_exc(e)
                    break

        except:
            print('buy_th ERROR')


    def give_balance(message):
        try:
            balance = func.GiveBalance(message.text)
            balance_dict[message.chat.id] = balance

            msg = bot.send_message(chat_id=message.chat.id,
                                   text='Введите сумму на которую изменится баланс(к балансу не добавится эта сумма, а баланс изменится на неё)')

            bot.register_next_step_handler(msg, give_balance_2)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Что-то пошло не по плану',
                             reply_markup=menu.main_menu())

    def give_balance_2(message):
        try:
            balance = balance_dict[message.chat.id]
            balance.balance = message.text
            msg = bot.send_message(chat_id=message.chat.id,
                                   text=f'ID - {balance.login}\n'
                                        f'Баланс изменится на - {balance.balance}\n'
                                        f'Для подтверждения введите +')

            bot.register_next_step_handler(msg, give_balance_3)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Что-то пошло не по плану',
                             reply_markup=menu.main_menu())

    def give_balance_3(message):
        try:
            balance = balance_dict[message.chat.id]
            if message.text == '+':
                func.give_balance(balance)
                bot.send_message(chat_id=message.chat.id,
                                 text='✅ Баланс успешно изменён')

        except Exception as e:
            bot.send_message(chat_id=message.chat.id,
                             text='⚠️ Что-то пошло не по плану',
                             reply_markup=menu.main_menu())


    def email_sending_photo(message):
        chat_id = message.chat.id
        try:
            file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            admin_sending = func.Admin_sending_messages(message.chat.id)
            func.admin_sending_messages_dict[message.chat.id] = admin_sending

            admin_sending = func.admin_sending_messages_dict[message.chat.id]
            admin_sending.photo = random.randint(111111, 999999)
            admin_sending.type_sending = 'photo'

            with open(f'photo/{admin_sending.photo}.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)

            msg = bot.send_message(
                chat_id=chat_id,
                text='Введите текст рассылки'
            )

            bot.register_next_step_handler(msg, email_sending_photo2)
        except Exception as e:
            traceback.print_exc(e)
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def email_sending_photo2(message):
        chat_id = message.chat.id
        try:

            admin_sending = func.admin_sending_messages_dict[message.chat.id]
            admin_sending.text = message.text

            with open(f'photo/{admin_sending.photo}.jpg', 'rb') as photo:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=admin_sending.text
                )
            
            msg = bot.send_message(
                chat_id=chat_id,
                text='Выбирите дальнейшее действие',
                reply_markup=menu.admin_sending
            )

            bot.register_next_step_handler(msg, email_sending_photo3)
        except:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def email_sending_photo3(message):
        chat_id = message.chat.id
        try:
            admin_sending = func.admin_sending_messages_dict[message.chat.id]
            if message.text in menu.admin_sending_btn:
                if message.text == menu.admin_sending_btn[0]: # Начать
                    conn = sqlite3.connect('base.db')
                    cursor = conn.cursor()
                    cursor.execute(f'SELECT * FROM users')
                    row = cursor.fetchall()
                    start_time = time.time()
                    amount_message = 0
                    amount_bad = 0

                    try:
                        bot.send_message(
                            chat_id=func.admin_id_manager().split(':')[0],
                            text=f'✅ Вы запустили рассылку',
                            reply_markup=menu.admin_menu)
                    except: pass

                    
                    for i in range(len(row)):
                        try:
                            with open(f'photo/{admin_sending.photo}.jpg', 'rb') as photo:
                                bot.send_photo(
                                    chat_id=row[i][0],
                                    photo=photo,
                                    caption=admin_sending.text,
                                    parse_mode='html')
                            amount_message += 1
                        except:
                            amount_bad += 1
                    
                    sending_time = time.time() - start_time

                    try:
                        bot.send_message(
                            chat_id=func.admin_id_manager().split(':')[0],
                            text=f'✅ Рассылка окончена\n'
                            f'❕ Отправлено: {amount_message}\n'
                            f'❕ Не отправлено: {amount_bad}\n'
                            f'🕐 Время выполнения рассылки - {sending_time} секунд'
                            
                            )              
                    except:
                        print('ERROR ADMIN SENDING')
                    try:
                        bot.send_message(
                            chat_id=func.admin_id_manager().split(':')[1],
                            text=f'✅ Рассылка окончена\n'
                            f'❕ Отправлено: {amount_message}\n'
                            f'❕ Не отправлено: {amount_bad}\n'
                            f'🕐 Время выполнения рассылки - {sending_time} секунд'
                            
                            )              
                    except:
                        print('ERROR ADMIN SENDING')
                elif message.text == menu.admin_sending_btn[1]: # Отложить
                    msg = bot.send_message(
                        chat_id=chat_id,
                        text="""
Введите дату начала рассылке в формате: ДЕНЬ:ЧАСОВ:МИНУТ\n

Например 18:14:10 - рассылка будет сделана 18 числа в 14:10
"""
                    )

                    bot.register_next_step_handler(msg, set_down_sending)
                elif message.text == menu.admin_sending_btn[2]:
                    bot.send_message(
                        message.chat.id, 
                        text='Рассылка отменена', 
                        reply_markup=menu.main_menu
                    )
                    bot.send_message(
                        message.chat.id, 
                        text='Меню админа', 
                        reply_markup=menu.admin_menu
                    )
            else:   
                msg = bot.send_message(
                    message.chat.id, 
                    text='Не верная команда, повторите попытку', 
                    reply_markup=menu.admin_sending)

                bot.register_next_step_handler(msg, email_sending_photo3)
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')

    
    def set_down_sending(message):
        admin_sending = func.admin_sending_messages_dict[message.chat.id]
        date = message.text
        admin_sending.date = date

        if int(date.split(':')[0]) > 0 and int(date.split(':')[0]) < 33:
            if int(date.split(':')[1]) >= 0 and int(date.split(':')[1]) <= 24:
                if int(date.split(':')[2]) >= 0 and int(date.split(':')[2]) < 61:
                    msg = bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Для подтверждения рассылки в {date} отправьте +'
                    )

                    bot.register_next_step_handler(msg, set_down_sending_2)

    def set_down_sending_2(message):
        if message.text == '+':
            admin_sending = func.admin_sending_messages_dict[message.chat.id]

            func.add_sending(admin_sending)

            bot.send_message(
                chat_id=message.chat.id,
                text=f'Рассылка запланирована в {admin_sending.date}',
                reply_markup=menu.admin_menu
            )
        else:
            bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=menu.admin_menu)

    def admin_sending_messages(message):
        admin_sending = func.Admin_sending_messages(message.chat.id)
        func.admin_sending_messages_dict[message.chat.id] = admin_sending

        admin_sending = func.admin_sending_messages_dict[message.chat.id]
        admin_sending.text = message.text

        msg = bot.send_message(
            chat_id=message.chat.id,
            text='Выбирите дальнейшее действие',
            reply_markup=menu.admin_sending)

        bot.register_next_step_handler(msg, admin_sending_messages_2)


    def admin_sending_messages_2(message):
        chat_id = message.chat.id

        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()

        admin_sending = func.admin_sending_messages_dict[message.chat.id]
        admin_sending.type_sending = 'text'

        if message.text in menu.admin_sending_btn:
            if message.text == menu.admin_sending_btn[0]: # Начать
                cursor.execute(f'SELECT * FROM users')
                row = cursor.fetchall()
                start_time = time.time()
                amount_message = 0
                amount_bad = 0

                try:
                    bot.send_message(
                        chat_id=func.admin_id_manager().split(':')[0],
                        text=f'✅ Вы запустили рассылку',
                        reply_markup=menu.admin_menu)
                except: pass

                for i in range(len(row)):
                    try:
                        bot.send_message(row[i][0], admin_sending.text, parse_mode='html')
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1
                
                sending_time = time.time() - start_time

                try:
                    bot.send_message(
                        chat_id=func.admin_id_manager().split(':')[0],
                        text=f'✅ Рассылка окончена\n'
                        f'❕ Отправлено: {amount_message}\n'
                        f'❕ Не отправлено: {amount_bad}\n'
                        f'🕐 Время выполнения рассылки - {sending_time} секунд'
                        
                        )              
                except:
                    print('ERROR ADMIN SENDING')
                try:
                    bot.send_message(
                        chat_id=func.admin_id_manager().split(':')[1],
                        text=f'✅ Рассылка окончена\n'
                        f'❕ Отправлено: {amount_message}\n'
                        f'❕ Не отправлено: {amount_bad}\n'
                        f'🕐 Время выполнения рассылки - {sending_time} секунд'
                        
                        )              
                except:
                    print('ERROR ADMIN SENDING')
            elif message.text == menu.admin_sending_btn[1]: # Отложить
                msg = bot.send_message(
                    chat_id=chat_id,
                    text="""
Введите дату начала рассылке в формате: ДЕНЬ:ЧАСОВ:МИНУТ\n

Например 18:14:10 - рассылка будет сделана 18 числа в 14:10
"""
                )

                bot.register_next_step_handler(msg, set_down_sending)
            elif message.text == menu.admin_sending_btn[2]:
                bot.send_message(
                    message.chat.id, 
                    text='Рассылка отменена', 
                    reply_markup=menu.main_menu
                )
                bot.send_message(
                    message.chat.id, 
                    text='Меню админа', 
                    reply_markup=menu.admin_menu
                )
            else:   
                msg = bot.send_message(
                    message.chat.id, 
                    text='Не верная команда, повторите попытку', 
                    reply_markup=menu.admin_sending)

    def admin_buttons_add(message):
        try:
            btn_dict = func.AdminButtons(message.chat.id)
            func.admin_buttons_dict[message.chat.id] = btn_dict
            btn_dict = func.admin_buttons_dict[message.chat.id]
            btn_dict.name = message.text

            msg = bot.send_message(
                chat_id=message.chat.id,
                text='Введите текст')

            bot.register_next_step_handler(msg, admin_buttons_add2)

        except Exception as e:
            pass
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_buttons_add2(message):
        try:
            btn_dict = func.admin_buttons_dict[message.chat.id]
            btn_dict.info = message.text

            msg = bot.send_message(
                chat_id=message.chat.id,
                text='Отправьте фото')

            bot.register_next_step_handler(msg, admin_buttons_add3)

        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')

    
    def admin_buttons_add3(message):
        try:
            btn_dict = func.admin_buttons_dict[message.chat.id]
            btn_dict.photo = str(random.randint(11111, 99999))

            file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(f'{btn_dict.photo}.jpg', 'wb') as new_file:
                new_file.write(downloaded_file)

            msg = bot.send_message(
                chat_id=message.chat.id,
                text='Для создания кнопки напишите +')

            bot.register_next_step_handler(msg, admin_buttons_add4)

        except Exception as e:
            pass
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_buttons_add4(message):
        try:
            btn_dict = func.admin_buttons_dict[message.chat.id]

            func.admin_add_btn(btn_dict.name, btn_dict.info, btn_dict.photo)

            bot.send_message(
                chat_id=message.chat.id,
                text='Кнопка создана',
                reply_markup=menu.admin_menu)

        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_buttons_del(message):
        try:
            func.admin_del_btn(message.text)

            bot.send_message(
                chat_id=message.chat.id,
                text='Кнопка удалена',
                reply_markup=menu.admin_menu)

        except Exception as e:
            print(e)
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_numbers_set_price(message):
        try:
            set_price = func.Admin_set_price(message.chat.id)
            func.admin_set_price[message.chat.id] = set_price
            set_price = func.admin_set_price[message.chat.id]
            
            info = func.get_countries_list(int(message.text))

            set_price.service = info[0]

            msg = bot.send_message(
                chat_id=message.chat.id,
                text=f'Введите номер страны для которой хотите изменить цену:\n\n{info[1]}'
            )
            bot.register_next_step_handler(msg, admin_numbers_set_price_2)
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_numbers_set_price_2(message):
        try:
            set_price = func.admin_set_price[message.chat.id]
            set_price.country = int(message.text)

            msg = bot.send_message(
                chat_id=message.chat.id,
                text=f'Введите цену'
            )
            bot.register_next_step_handler(msg, admin_numbers_set_price_3)

        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')


    def admin_numbers_set_price_3(message):
        try:
            set_price = func.admin_set_price[message.chat.id]
            set_price.price = float(message.text)

            if func.change_price_number(set_price) == True:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'✅ Цена успешно изменена на {set_price.price} ₽',
                    reply_markup=menu.admin_numbers
                )
        except Exception as e:
            bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Что-то пошло не по плану')

    def check_payouts():
        while True:
            try:
                time.sleep(5)

                conn = sqlite3.connect('btc.db')
                cursor = conn.cursor()

                cursor.execute(f'SELECT * FROM payouts')
                payouts = cursor.fetchall()

                if len(payouts) > 0:
                    for i in payouts:
                        if i[1] == 'bad':
                            cursor.execute(f'DELETE FROM payouts WHERE user_id = "{i[0]}"')
                            conn.commit()

                            bot.send_message(chat_id=i[0],
                                             text=f'✅ Ваш чек проверен, на ваш баланс начислено 0 ₽',
                                             reply_markup=menu.to_close)
                        else:
                            cursor.execute(f'DELETE FROM payouts WHERE user_id = "{i[0]}"')
                            conn.commit()

                            User(i[0]).update_balance(i[1])

                            bot.send_message(chat_id=i[0],
                                             text=f'✅ Ваш чек проверен, на ваш баланс начислено +{i[1]} ₽',
                                             reply_markup=menu.to_close)
            except:
                pass

    threading.Thread(target=btc.check_btc).start()
    threading.Thread(target=check_payouts).start()
    
    threading.Thread(target=sending_check).start()

    bot.polling(none_stop=True)
    


start_bot()
