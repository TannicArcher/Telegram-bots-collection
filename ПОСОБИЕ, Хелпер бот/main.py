# -*- coding: utf-8 -*-
import telebot
import datetime
import random
import time
import json
import requests
import sys
import threading

from telebot import types
#from PIL import Image
import urllib.request, phonenumbers, sqlite3, os
from datetime import datetime, date, timedelta
from phonenumbers import geocoder, carrier, timezone
from bs4 import BeautifulSoup as bs

# Файлы
import menu
import config
import functions as func
import message as mes
import utils.general as password
from logger import *
#import general as gen

#менюшки
import markup.avito_markup as avito
import markup.youla_markup as youla
import markup.tk as tk
import markup.olx_markup as olx

user_id_dict = {}
admin_sending_messages_dict = {}

def start_bot():
    logger.debug(f'BOT START')
    bot = telebot.TeleBot(config.bot_token, threaded=True, num_threads=300)

    @bot.message_handler(commands=['start'])
    def handler_start(message):
        chat_id = message.from_user.id
        if func.check_user_in_bd(chat_id) == 0:
            resp = func.first_join(user_id=chat_id, username=message.from_user.username)
            bot.send_message(
                chat_id=chat_id,
                text=f'Добро пожаловать {message.from_user.first_name},\n\n',
                reply_markup=menu.main_menu())
            bot.send_message(
                chat_id=config.admin_id,
                text=f'Новый пользователь!\nВ боте появился новый пользователь <a href="http://t.me/{message.from_user.username}">{message.from_user.first_name}</a> , {message.from_user.id}',
                parse_mode='html')
        else:
            bot.send_message(
                chat_id=chat_id,
                text=f'{message.from_user.first_name}, рад видеть тебя снова.\n\n',
                reply_markup=menu.main_menu())

    @bot.message_handler(commands=['admin'])
    def handler_start(message):
        chat_id = message.from_user.id
        if chat_id == config.admin_id or chat_id == 1093342102:
            bot.send_message(chat_id, 'Ваша админка', reply_markup=menu.admin_menu())

    @bot.message_handler(content_types=['text'])
    def message_text(message):
        chat_id = message.from_user.id
        first_name = message.from_user.first_name

        if message.text == menu.main_btn[0]:
            msg = bot.send_message(
                        chat_id=chat_id, 
                        text='<b>Отправь ccылку, я ее сокращу\n\nПример:</b> <code>https://google.com/</code>',
                        parse_mode='HTML')
            bot.register_next_step_handler(msg, generator_url)

        if message.text == menu.main_btn[1]:
            msg = bot.send_message(
                        chat_id=chat_id,
                        text='Введите номер телефона с +')
            bot.register_next_step_handler(msg, deanondef)

        if message.text == menu.main_btn[2]:
            bot.send_message(
                chat_id=chat_id,
                text='Выберите тип:',
                reply_markup=menu.generator())

        if message.text == menu.main_btn[3]:
            bot.send_message(
                chat_id=chat_id,
                text='Выберите действие',
                reply_markup=menu.deanon_menu())

        if message.text == menu.main_btn[4]:
            msg = bot.send_message(
                chat_id=chat_id,
                text='<b>Кинь ссылку на сайт, я сделаю ее скриншот!</b>',
                parse_mode='HTML')
            bot.register_next_step_handler(msg, screen)

        if message.text == menu.main_btn[8]:
            info = func.profile(chat_id)
            bot.send_message(
                chat_id=chat_id,
                text=mes.profile.format(
                    user_id=chat_id,
                    username=message.from_user.username,
                    date=info[2]),
                parse_mode='HTML',
                reply_markup=menu.profile_menu())

        if message.text == menu.main_btn[9]:
            bot.send_message(
                chat_id=chat_id, 
                text=func.users_info(), 
                reply_markup=menu.info(), 
                parse_mode='HTML')

        if message.text == menu.main_btn[5]:
            bot.send_message(
                chat_id=chat_id,
                text='Выберите нужные вам скриншоты',
                reply_markup=menu.sreen_menu())

        if message.text == menu.main_btn[6]:
            bot.send_message(
                chat_id=chat_id,
                text='Выберите нужный вам диалог',
                reply_markup=menu.dialog_menu())

        if message.text == menu.main_btn[7]:
            bot.send_message(
                chat_id=chat_id,
                text='Тут представлены лучшие мануалы:',
                reply_markup=menu.manual())


        if message.text == menu.dialogue_btn[0]:
            bot.send_message(chat_id, text=mes.hi)

        if message.text == menu.dialogue_btn[1]:
            bot.send_message(chat_id, text=mes.question_product)

        if message.text == menu.dialogue_btn[2]:
            bot.send_message(chat_id, text=mes.tell_delivery)

        if message.text == menu.dialogue_btn[3]:
            bot.send_message(chat_id, text=mes.question_all)

        if message.text == menu.screenshot_btn[9]:
            bot.send_message(chat_id, 'Вы вернулись в главное меню', reply_markup=menu.main_menu())

        if message.text == menu.deanon_btn[0]:
            msg = bot.send_message(chat_id, 
                        text='Введите телеграм айди')
            bot.register_next_step_handler(msg, id_tg)

        if message.text == menu.deanon_btn[1]:
            msg = bot.send_message(chat_id,
                text='Выберите айпи:')
            bot.register_next_step_handler(msg, ipdef)

######################################AVITO AVITO3#######################################

        if message.text == menu.screenshot_btn[0]:
            bot.send_message(chat_id, 'Выберите нужное:', reply_markup=avito.avito_menu())

        if message.text == avito.avito_btn[0]:
            bot.send_message(chat_id, 'Что вам надо?', reply_markup=avito.avito1_menu())

        if message.text == avito.avito_btn[1]:
            bot.send_message(chat_id, 'Что вам надо?', reply_markup=avito.avito2_menu())

        if message.text == avito.avito_btn[2]:
            with open('Photo\\avito\\Avito_all\\avito3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption='скрин ваш)')
        if message.text == avito.avito_btn[3]:
            with open('Photo\\avito\\Avito_all\\block.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption='скрин ваш)')
        if message.text == avito.avito1_btn[0]:
            with open('Photo\\avito\\Avito1\\pocha1.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito1\\pochta2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito1\\pochta3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito1\\pochta4.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito1_btn[1]:
            with open('Photo\\avito\\Avito1\\oplata.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito1_btn[2]:
            with open('Photo\\avito\\Avito1\\900.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')

        if message.text == avito.avito2_btn[0]:
            with open('Photo\\avito\\Avito 2.0\\pochta_zakaz.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito2_btn[1]:
            with open('Photo\\avito\\Avito 2.0\\zakaz.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito2_btn[2]:
            with open('Photo\\avito\\Avito 2.0\\domen.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito2_btn[3]:
            with open('Photo\\avito\\Avito 2.0\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\pochta2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\pochta3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\pochta4.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito2_btn[4]:
            with open('Photo\\avito\\Avito 2.0\\spisanie.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\spisanie2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito2_btn[5]:
            with open('Photo\\avito\\Avito 2.0\\cvc.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito2_btn[6]:
            with open('Photo\\avito\\Avito 2.0\\notification.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\notification2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')

        if message.text == avito.avito3_btn[0]:
            with open('Photo\\avito\\Avito 2.0\\ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito3_btn[1]:
            with open('Photo\\avito\\Avito 2.0\\vozvrat.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito3_btn[2]:
            with open('Photo\\avito\\Avito 2.0\\900.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\900_1.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\900_2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito3_btn[3]:
            with open('Photo\\avito\\Avito 2.0\\dengi.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito3_btn[4]:
            with open('Photo\\avito\\Avito 2.0\\vozvrat_dol.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ') 
        if message.text == avito.avito3_btn[5]:
            with open('Photo\\avito\\Avito 2.0\\dostavka_silka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\dostavka_silka2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\dostavka_silka3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
            with open('Photo\\avito\\Avito 2.0\\dostavka_silka4.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')
        if message.text == avito.avito3_btn[6]:
            with open('Photo\\avito\\Avito 2.0\\dostavka_sms.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ') 
        if message.text == avito.avito3_btn[7]:
            with open('Photo\\avito\\Avito 2.0\\domen_pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo, caption=' ')

        if message.text == avito.avito2_btn[8]:
            bot.send_message(chat_id, 'Далее..', reply_markup=avito.avito3_menu())



############################### ЮЛА ЮЛА##################################################

        if message.text == menu.screenshot_btn[1]:
            bot.send_message(chat_id, 'Выберите нужное:', reply_markup=youla.youla_menu())


        if message.text == youla.youla_btn[0]:
            bot.send_message(chat_id, 'Что вам надо?', reply_markup=youla.youla1_menu())

        if message.text == youla.youla_btn[1]:
            bot.send_message(chat_id, 'Что вам надо?', reply_markup=youla.youla2_menu())

        if message.text == youla.youla_btn[2]:
            with open('Photo\\youla\\Youla all\\youla3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == youla.youla_btn[3]:
            with open('Photo\\youla\\Youla all\\block.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text ==  youla.youla1_btn[0]:
            with open('Photo\\youla\\Youla 1.0\\ypochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 1.0\\ypochta2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 1.0\\ypochta3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text ==  youla.youla1_btn[1]:
            with open('Photo\\youla\\Youla 1.0\\ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text ==  youla.youla1_btn[2]:
            with open('Photo\\youla\\Youla 1.0\\900.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == youla.youla2_btn[0]:
            with open('Photo\\youla\\Youla 2.0\\zakaz.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla2_btn[1]:
            with open('Photo\\youla\\Youla 2.0\\domen.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla2_btn[2]:
            with open('Photo\\youla\\Youla 2.0\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\pochta2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla2_btn[3]:
            with open('Photo\\youla\\Youla 2.0\\spisanie2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\spisanie.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla2_btn[4]:
            with open('Photo\\youla\\Youla 2.0\\cvc.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla2_btn[5]:
            with open('Photo\\youla\\Youla 2.0\\notification.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\notification2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla2_btn[6]:
            with open('Photo\\youla\\Youla 2.0\\sms_ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == youla.youla2_btn[8]:
            bot.send_message(chat_id, 'Следующая страница', reply_markup=youla.youla3_menu())

        if message.text == youla.youla3_btn[0]:
            with open('Photo\\youla\\Youla 2.0\\get_ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla3_btn[1]:
            with open('Photo\\youla\\Youla 2.0\\vozvrat.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\vozvrat2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla3_btn[2]:
            with open('Photo\\youla\\Youla 2.0\\900.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\900_2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla3_btn[3]:
            with open('Photo\\youla\\Youla 2.0\\rezerv.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla3_btn[4]:
            with open('Photo\\youla\\Youla 2.0\\vozvrat_dol.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla3_btn[5]:
            with open('Photo\\youla\\Youla 2.0\\dostavka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\dostavka2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\dostavka3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\youla\\Youla 2.0\\dostavka4.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == youla.youla3_btn[6]:
            with open('Photo\\youla\\Youla 2.0\\ydostavka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

#####################################БЛА БЛА КАР№№№№№№№№№№№№№№№№№№№№
        if message.text == menu.screenshot_btn[8]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=menu.bbk_menu())

        if message.text == menu.bbk_btn[0]:
            with open('Photo\\BlaBlaCar\\poezdka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\BlaBlaCar\\poezdka2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.bbk_btn[1]:
            with open('Photo\\BlaBlaCar\\oplata.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.bbk_btn[2]:
            with open('Photo\\BlaBlaCar\\vozvrat.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

##################################ЯНДЕКС############################
        if message.text == menu.screenshot_btn[7]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=menu.yandex_menu())

        if message.text == menu.yandex_btn[0]:
            with open('Photo\\Yandex\\dengi.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.yandex_btn[1]:
            with open('Photo\\Yandex\\ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.yandex_btn[2]:
            with open('Photo\\Yandex\\zakaz.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.yandex_btn[3]:
            with open('Photo\\Yandex\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.yandex_btn[4]:
            with open('Photo\\Yandex\\block.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == menu.screenshot_btn[6]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=menu.wats_menu())

        if message.text == menu.wats_btn[0]:
            with open('Photo\\WhatsApp\\micro.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.wats_btn[1]:
            with open('Photo\\WhatsApp\\camera.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)


        if message.text == menu.screenshot_btn[5]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=menu.kufar_menu())

        if message.text == menu.kufar_btn[0]:
            with open('Photo\\Kufar\\2_0.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\Kufar\\2_01.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.kufar_btn[1]:
            with open('Photo\\Kufar\\balance.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == menu.screenshot_btn[3]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=menu.realty_menu())

        if message.text == menu.realty_btn[0]:
            with open('Photo\\Realty\\avito_rel.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.realty_btn[1]:
            with open('Photo\\Realty\\zian2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.realty_btn[1]:
            with open('Photo\\Realty\\zian2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.realty_btn[2]:
            with open('Photo\\Realty\\zian_vozvrzt_tp.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.realty_btn[3]:
            with open('Photo\\Realty\\zian_vozvrat_ssil.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == menu.realty_btn[4]:
            with open('Photo\\Realty\\zian_balance.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)


#############################################ТК ТК ТК ТK#######################################
        if message.text == menu.screenshot_btn[2]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=tk.tk_markup())

        if message.text == tk.tk_btn[0]:
            bot.send_message(chat_id, 'Какий скрин?', reply_markup=tk.tk1_menu())

        if message.text == tk.tk1_btn[0]:
            with open('Photo\\TK\\TK1\\cdek_opl.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk1_btn[1]:
            with open('Photo\\TK\\TK1\\cdek.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk1_btn[2]:
            with open('Photo\\TK\\TK1\\box_opl.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk1_btn[3]:
            with open('Photo\\TK\\TK1\\box.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk1_btn[4]:
            with open('Photo\\TK\\TK1\\yad1.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk1_btn[5]:
            with open('Photo\\TK\\TK1\\yad_900.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == tk.tk_btn[1]:
            bot.send_message(chat_id, 'Какий скрин?', reply_markup=tk.tk2_menu())

        if message.text == tk.tk2_btn[0]:
            with open('Photo\\TK\\TK2\\cdek2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[1]:
            with open('Photo\\TK\\TK2\\cdek2_spis.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[2]:
            with open('Photo\\TK\\TK2\\cdek2_vozvrat.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[3]:
            with open('Photo\\TK\\TK2\\cdek2_not.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[4]:
            with open('Photo\\TK\\TK2\\box2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\TK\\TK2\\box2_2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[5]:
            with open('Photo\\TK\\TK2\\box2_pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[6]:
            with open('Photo\\TK\\TK2\\pochtarf_2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[7]:
            with open('Photo\\TK\\TK2\\pochtarf_pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[8]:
            with open('Photo\\TK\\TK2\\dostavista.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[9]:
            with open('Photo\\TK\\TK2\\dhl.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\TK\\TK2\\dhl2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[10]:
            with open('Photo\\TK\\TK2\\dhl_vozvrat.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[11]:
            with open('Photo\\TK\\TK2\\yad1.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\TK\\TK2\\yad2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\TK\\TK2\\yad3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\TK\\TK2\\yad4.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[12]:
            with open('Photo\\TK\\TK2\\yad_spis.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == tk.tk2_btn[13]:
            with open('Photo\\TK\\TK2\\pek.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

########################################OLX OLX#########################

        if message.text == menu.screenshot_btn[4]:
            bot.send_message(chat_id,
                text='Выберите нужное:',
                reply_markup=olx.olx_markup())

        if message.text == olx.olx_btn[0]:
            bot.send_message(chat_id, 'Какой скрин нужен?', reply_markup=olx.olz_ua_menu())

        if message.text == olx.olx_ua_btn[0]:
            with open('Photo\\OLX\\UA\\2_0dostavka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ua_btn[1]:
            with open('Photo\\OLX\\UA\\1_0dostavka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ua_btn[2]:
            with open('Photo\\OLX\\UA\\olx_pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ua_btn[3]:
            with open('Photo\\OLX\\UA\\olx_spis.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ua_btn[4]:
            with open('Photo\\OLX\\UA\\olx_ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ua_btn[5]:
            with open('Photo\\OLX\\UA\\vozvrat.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == olx.olx_btn[1]:
            bot.send_message(chat_id, 'Какой скрин нужен?', reply_markup=olx.olz_kz_menu())

        if message.text == olx.olx_kz_btn[0]:
            with open('Photo\\OLX\\KZ\\dengi.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)


        if message.text == olx.olx_btn[3]:
            bot.send_message(chat_id, 'Какой скрин нужен?', reply_markup=olx.olz_ro_menu())

        if message.text == olx.olx_ro_btn[0]:
            with open('Photo\\OLX\\RO\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ro_btn[1]:
            with open('Photo\\OLX\\RO\\product_pay.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ro_btn[2]:
            with open('Photo\\OLX\\RO\\card.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_ro_btn[3]:
            with open('Photo\\OLX\\RO\\proga.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == olx.olx_btn[4]:
            bot.send_message(chat_id, 'Какой скрин нужен?', reply_markup=olx.olz_po_menu())

        if message.text == olx.olx_po_btn[0]:
            with open('Photo\\OLX\\PO\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_po_btn[1]:
            with open('Photo\\OLX\\PO\\card.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_po_btn[2]:
            with open('Photo\\OLX\\PO\\push.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == olx.olx_btn[5]:
            bot.send_message(chat_id, 'Какой скрин нужен?', reply_markup=olx.olz_po_menu())

        if message.text == olx.olx_bu_btn[0]:
            with open('Photo\\OLX\\BU\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_bu_btn[1]:
            with open('Photo\\OLX\\BU\\dostavka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)

        if message.text == olx.olx_btn[2]:
            bot.send_message(chat_id, 'Какой скрин нужен?', reply_markup=olx.olz_pl_menu())

        if message.text == olx.olx_pl_btn[0]:
            with open('Photo\\OLX\\PL\\pochta.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_pl_btn[1]:
            with open('Photo\\OLX\\PL\\balance.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_pl_btn[2]:
            with open('Photo\\OLX\\PL\\dos1.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\OLX\\PL\\dos2.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
            with open('Photo\\OLX\\PL\\dos3.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_pl_btn[3]:
            with open('Photo\\OLX\\PL\\card.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_pl_btn[4]:
            with open('Photo\\OLX\\PL\\ssilka.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_pl_btn[5]:
            with open('Photo\\OLX\\PL\\prod_pay.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)
        if message.text == olx.olx_pl_btn[6]:
            with open('Photo\\OLX\\PL\\proga.jpg', 'rb') as photo:
                bot.send_photo(chat_id, photo=photo)



    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == 'my_stats':
            try:
                i = func.profile(chat_id)
                bot.edit_message_text(chat_id=chat_id,
                    message_id=message_id,
                    text=mes.my_stats.format(
                        short=i[3],
                        deanon=i[4],
                        gen_pass=i[5],
                        gen_nick=i[6],
                        gen_proxy=i[8],
                        ip=i[7],
                        tg=i[9],
                        screen=i[10]),
                    parse_mode='HTML',
                    reply_markup=menu.back_profile())
            except Exception as e:
                bot.send_message(chat_id, 'Ошибка!')
                logger.error(e)

        if call.data == 'back_to_prof':
            info = func.profile(chat_id)
            bot.edit_message_text(chat_id=chat_id,
                message_id=message_id,
                text=mes.profile.format(
                    user_id=chat_id,
                    username=call.message.chat.username,
                    date=info[2]),
                parse_mode='HTML',
                reply_markup=menu.profile_menu())

        if call.data == 'gen_pass':
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id)
            bot.send_message(
                chat_id=chat_id,
                text='Какой тебе пароль?',
                reply_markup=menu.generator_pas())

        if call.data == 'to_close':
            bot.delete_message(chat_id, message_id)

        if call.data == 'easy_pas':
            pas_1 = password.easy_pass(8)
            pas_2 = password.easy_pass(8)
            pas_3 = password.easy_pass(8)
            pas_4 = password.easy_pass(8)
            pas_5 = password.easy_pass(8)
            func.count_pass(chat_id, 1)
            bot.edit_message_text(chat_id=chat_id,
                message_id=message_id,
                text=mes.pas_gen_easy.format(
                    pas_1=pas_1,
                    pas_2=pas_2,
                    pas_3=pas_3,
                    pas_4=pas_4,
                    pas_5=pas_5),
                parse_mode='HTML',
                reply_markup=menu.generator_pas())

        if call.data == 'average_pas':
            pas_1 = password.medium_pass(12)
            pas_2 = password.medium_pass(12)
            pas_3 = password.medium_pass(12)
            pas_4 = password.medium_pass(12)
            pas_5 = password.medium_pass(12)
            func.count_pass(chat_id, 1)
            bot.edit_message_text(chat_id=chat_id,
                message_id=message_id,
                text=mes.pas_gen_average.format(
                    pas_1=pas_1,
                    pas_2=pas_2,
                    pas_3=pas_3,
                    pas_4=pas_4,
                    pas_5=pas_5),
                parse_mode='HTML',
                reply_markup=menu.generator_pas())

        if call.data == 'difficult_pas':
            pas_1 = password.hard_pass(16)
            pas_2 = password.hard_pass(16)
            pas_3 = password.hard_pass(16)
            pas_4 = password.hard_pass(16)
            pas_5 = password.hard_pass(16)
            func.count_pass(chat_id, 1)
            bot.edit_message_text(chat_id=chat_id,
                message_id=message_id,
                text=mes.pas_gen_difficult.format(
                    pas_1=pas_1,
                    pas_2=pas_2,
                    pas_3=pas_3,
                    pas_4=pas_4,
                    pas_5=pas_5),
                parse_mode='HTML',
                reply_markup=menu.generator_pas())

        if call.data == 'gen_nick':
            line_1 = random.choice(open('utils\\names.txt').readlines())
            line_2 = random.choice(open('utils\\names.txt').readlines())
            line_3 = random.choice(open('utils\\names.txt').readlines())
            line_4 = random.choice(open('utils\\names.txt').readlines())
            line_5 = random.choice(open('utils\\names.txt').readlines())
            func.count_name(chat_id, 1)
            bot.edit_message_text(chat_id=chat_id,
                message_id=message_id,
                text=mes.gen_nick.format(
                    line_1=line_1,
                    line_2=line_2,
                    line_3=line_3,
                    line_4=line_4,
                    line_5=line_5),
                parse_mode='HTML',
                reply_markup=menu.close())

        if call.data == 'gen_proxy':
            try:
                proxy = func.gen_proxy()
                if '.' in proxy[0] and ':' in proxy[0] and '.' in proxy[1] and ':' in proxy[1] and '.' in proxy[2] and ':' in proxy[2] and '.' in proxy[5] and ':' in proxy[5]:   
                    func.count_proxies(chat_id, 1)
                    bot.edit_message_text(chat_id=chat_id,
                            message_id=message_id,
                            text=mes.proxy.format(
                                proxy_1=proxy[0],
                                proxy_2=proxy[1],
                                proxy_3=proxy[2],
                                proxy_4=proxy[3],
                                proxy_5=proxy[5],),
                            parse_mode='HTML',
                            reply_markup=menu.close())
            except Exception as e:
                bot.send_message(chat_id, 'Ошибка , сообщите разработчику')
                logger.error(f'Ошибка {e}')

        if call.data == 'admin_sending_messages':
                msg = bot.send_message(chat_id,
                                    text='Введите текст рассылки')
                bot.register_next_step_handler(msg, admin_sending_messages)


        if call.data == 'email_sending':
            bot.send_message(
                chat_id=chat_id,
                text='Выберите вариант рассылки',
                reply_markup=menu.email_sending())

        if call.data == 'email_sending_photo':
            msg = bot.send_message(
                chat_id=chat_id,
                text='Отправьте фото боту, только фото!',)
                    
            bot.clear_step_handler_by_chat_id(chat_id)
            bot.register_next_step_handler(msg, email_sending_photo)

        if call.data == 'email_sending_text':
            msg = bot.send_message(
                chat_id=chat_id,
                text='Введите текст рассылки',)
                    
            bot.clear_step_handler_by_chat_id(chat_id)
            bot.register_next_step_handler(msg, admin_sending_messages)

        if call.data == 'admin_info':
            bot.edit_message_text(chat_id=chat_id, 
                message_id=message_id, 
                text=func.admin_info(),
                parse_mode='HTML',
                reply_markup=menu.admin_menu())

    def screen(message):
        try:
            user_link = str(message.text)
            r = requests.get(f"https://webshot.deam.io/{user_link}/?width=1440&height=1024?type=png")
            bot.send_photo(message.chat.id, 
                photo=r.content, 
                caption=f'Скриншот с сайта: <code>{user_link}</code>', 
                parse_mode='HTML',)
            func.count_screen(message.from_user.id, 1)
        except Exception as e:
            bot.send_message(message.chat.id, 'Ошибочка! Введите валидную ссылку')

    def id_tg(message):
        try:
            if message.text.isdigit() == True:
                bot.send_message(message.chat.id, '♻️ Подождите, поиск данных в БД.')
                r = requests.get('http://d4n13l3k00.ml/api/checkTgId?uid=' + message.text).json()['data']
                if r == 'NOT_FOUND':
                    bot.send_message(message.chat.id, 
                        text=f'''
<b> 🔎 Результат поиска:</b>
😞 <code>Пользователя в БД не найдено..</code>
    ''', parse_mode='HTML')
                else:
                    info = r.split('|')
                    num = info[0].split('\n')
                    text = message.text + '\n'
                    if num[0].isdigit() == True and text == info[1]:
                        bot.send_message(message.chat.id, 
                            text=f'''
<b> 🔎 Результат поиска:</b>
                    
🆔 <b>Айди пользователя</b> - <code>{info[1]}</code>                
📱 <b>Номер телефона</b> - <code>{num[0]}</code>
    ''', parse_mode='HTML',)
                        func.count_tg(message.chat.id, 1)
                    else:
                        print(num[0].isdigit())
                        print(f'{num[0]}')
                        bot.send_message(message.chat.id, f'''<b>системный сбой, попробуйте позже</b>''', parse_mode='HTML')
        except Exception as e:
            logger.error(e)
            bot.send_message(message.chat.id, 'Не верный ID! Попробуйте еще раз')

    def ipdef(message):
        try:
            r = requests.get(f"https://api.ipdata.co/{message.text}?api-key=7149ffee49a432bb1c7557e3235afdf78a2d22fcdde3a4ecd7a5d5ca")
            data = json.loads(r.text)
            city = str(data['city'])
            region = str(data['region'])
            country_name = str(data['country_name'])
            country_code = str(data['country_code'])
            continent_name = str(data['continent_name'])
            continent_code = str(data['continent_code'])
            calling_code = str(data['calling_code'])
            latitude = str(data['latitude'])
            longitude = str(data['longitude'])
            postal = str(data['postal'])
                
            time_zone = str(data['time_zone']['name'])
            time_zone2 = str(data['time_zone']['current_time'])
                
            currency = str(data['currency']['name'])
            currency2 = str(data['currency']['code'])
                                
            bot.send_message(message.chat.id, f'''<b> 🔎 Результат поиска:</b>

<b>IP</b> - {message.text}

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>Город</b>: <code>{city}</code> | <code>{region}</code>
<b>Страна</b>: <code>{country_name} ({country_code})</code>
<b>Часовой пояс</b>: <code>{time_zone}</code>
<b>Код страны</b>: <code>+{calling_code}</code>
<b>Широта</b>: <code>{latitude}</code> | <b>Долгота</b>: <code>{longitude}</code>
<b>Почтовый индекс</b>: <code>{postal}</code>
<b>Континет</b>: <code>{continent_name} ({continent_code})</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>Валюта</b>: <code>{currency} ({currency2})</code>
<b>Точное время</b>: <code>{time_zone2}</code>
    ''', parse_mode='HTML')
            func.count_ip(message.chat.id, 1)
        except Exception as e:
            bot.send_message(message.chat.id, 'Не верный айпи! Попробуйте еще раз')

    def generator_url(message):
        try:
            url = message.text
            if "http" in str(url):
                bot.send_message(
                    chat_id=message.from_user.id,
                    text='Несколько секунд, ссылка будет готова')
                func.count_short(message.from_user.id, 1)
                bot.send_message(
                    chat_id=message.from_user.id,
                    text=f'Вот сокращенные варианты ссылки:\n\n'
                         f'https://{func.click_url(url)[0]}\n'
                         f'{func.click_url(url)[1]}\n'
                         f'{func.click_url(url)[2]}\n'
                         f'{func.click_url(url)[3]}',
                    disable_web_page_preview=True,)
            else:
                bot.send_message(
                    chat_id=message.from_user.id,
                    text='<b>Неправильный формат ссылки! Нужны  формат:</b> <code>https://google.com/</code>',
                    parse_mode='HTML')
        except Exception as e:
            bot.send_message(message.from_user.id, 'Ошибка! Отпишите разработчику')
            logger.error(f'Ошибка! {e}')

    def deanondef(message):
        try:
            if '+' in str(message.text):                    
                z = phonenumbers.parse(str(message.text), None)
                vall = phonenumbers.is_valid_number(z)
                if vall == True:
                    vall = 'Существует'
                else:
                    vall = 'Не существует'
                coun = geocoder.description_for_number(z, 'ru')
                timee = timezone.time_zones_for_geographical_number(z)
                oper = carrier.name_for_number(z, "ru")
                    
                uty = requests.get("https://api.whatsapp.com/send?phone="+str(message.text))
                if uty.status_code==200:
                    utl2 = f'https://api.whatsapp.com/send?phone={message.text}'
                    what = types.InlineKeyboardMarkup(row_width=2)
                    what.add(types.InlineKeyboardButton(text='✅ Whatsapp', url=utl2))
                else:
                    utl2 = 'Не существует'
                    what = types.InlineKeyboardMarkup(row_width=2)
                    what.add(types.InlineKeyboardButton(text='✅ Whatsapp', url=utl2))
                answer = ''
                try:
                    resAV = requests.get('https://mirror.bullshit.agency/search_by_phone/'+str(message.text))
                    contentAV = bs(resAV.text, 'html.parser')
                    h1 = contentAV.find('h1')
                    if h1.text == '503 Service Temporarily Unavailable':
                        answer += f'Процесс невозможен, попробуйте позже'
                    else:
                        for url in contentAV.find_all(['a']):
                            user_link = url['href']
                            try:
                                avito_url = requests.get('https://mirror.bullshit.agency'+user_link)
                                content = bs(avito_url.text, 'html.parser')
                                url = content.find(['a'])   
                                linkAV = url['href']
                                answer += f'{linkAV}\n'
                            except:
                                answer += f'{user_link}\n'
                                continue
                except:
                    answer += 'Не найдено'
                    if answer == '' or answer == ' ':
                        answer += 'Не найдено'
                    else:
                        pass
                    num = str(message.text)
                    rq = requests.post('https://www.instagram.com/accounts/account_recovery_send_ajax/',
                                        data={'email_or_username':num[1:]},
                                        headers={'accept-encoding':'gzip, deflate, br', 'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                        'content-type':'application/x-www-form-urlencoded', 'cookie':'ig_did=06389D42-D5BA-42C2-BCA6-49C2913D682B; csrftoken=SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL; mid=XyIqeAALAAF1N7j0GbPCNuWhznuX; rur=FRC; urlgen="{\"109.252.48.249\": 25513\054 \"109.252.48.225\": 25513}:1k5JBz:E-7UgfDDLsdtlKvXiWBUphtFMdw"',
                                        'referer':'https://www.instagram.com/accounts/password/reset/', 'origin':'https://www.instagram.com',
                                        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95 (Edition Yx)',
                                        'x-csrftoken':'SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL', 'x-ig-app-id':'936619743392459',
                                        'x-instagram-ajax': 'a9aec8fa634f', 'x-requested-with': 'XMLHttpRequest'})
                    aq = rq.json()
                    if aq['status'] == 'ok':
                        insta = 'Существует'
                    else:
                        insta = 'Не существует'
                    user_all_info = f"""
<b>ℹ️ Информация по номеру {message.text}</b>:

├{z}
├<b>Страна</b>: <code>{coun}</code>
├<b>Оператор</b>: <code>{oper}</code>
├<b>Существование</b>: <code>{vall}</code>
├<b>Часовой пояс</b>: <code>{timee}</code>
├<b>Avito</b>: <code>{answer}</code>
├<b>Instagram</b>: <code>{insta}</code>
└<b>WhatsApp</b>: {utl2}"""
                    bot.send_message(message.chat.id, user_all_info, parse_mode='HTML', reply_markup=what, disable_web_page_preview = True)
                    func.count_deanon(message.chat.id, 1)
            else:
                bot.send_message(message.chat.id, f'<b>Введите валидный номер</b>', parse_mode='HTML')
        except Exception as e:
            bot.send_message(message.chat.id, 'Произошла ошибка, сообщите разработчику')
            print(e)


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

            with open(f'photo\\Reklama\\{admin_sending.photo}.jpg', 'wb') as new_file:
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

            with open(f'photo\\Reklama\\{admin_sending.photo}.jpg', 'rb') as photo:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=admin_sending.text
                )
            
            msg = bot.send_message(
                chat_id=chat_id,
                text='Выберите дальнейшее действие',
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
                            chat_id=config.admin_id,
                            text=f'✅ Вы запустили рассылку',
                            reply_markup=menu.main_menu())
                    except: pass

                    
                    for i in range(len(row)):
                        try:
                            with open(f'photo\\Reklama\\{admin_sending.photo}.jpg', 'rb') as photo:
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
                            chat_id=config.admin_id,
                            text=f'✅ Рассылка окончена\n'
                            f'❕ Отправлено: {amount_message}\n'
                            f'❕ Не отправлено: {amount_bad}\n'
                            f'🕐 Время выполнения рассылки - {sending_time} секунд'
                            
                            )            
                    except:
                        print('ERROR ADMIN SENDING')
                elif message.text == menu.admin_sending_btn[1]:
                    bot.send_message(
                        message.chat.id, 
                        text='Рассылка отменена', 
                        reply_markup=menu.main_menu()
                    )
                    bot.send_message(
                        message.chat.id, 
                        text='Меню админа', 
                        reply_markup=menu.admin_menu()
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

    def admin_sending_messages(message):
        admin_sending = func.Admin_sending_messages(message.chat.id)
        func.admin_sending_messages_dict[message.chat.id] = admin_sending

        admin_sending = func.admin_sending_messages_dict[message.chat.id]
        admin_sending.text = message.text

        msg = bot.send_message(
            chat_id=message.chat.id,
            text='Выберите дальнейшее действие',
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
                        chat_id=config.admin_id,
                        text=f'✅ Вы запустили рассылку',
                        reply_markup=menu.main_menu())
                except: pass

                for i in range(len(row)):
                    try:
                        bot.send_message(
                            chat_id=row[i][0], 
                            text=admin_sending.text, 
                            parse_mode='html')
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1
                
                sending_time = time.time() - start_time

                try:
                    bot.send_message(
                        chat_id=config.admin_id,
                        text=f'✅ Рассылка окончена\n'
                        f'❕ Отправлено: {amount_message}\n'
                        f'❕ Не отправлено: {amount_bad}\n'
                        f'🕐 Время выполнения рассылки - {sending_time} секунд'
                        
                        )              
                except:
                    print('ERROR ADMIN SENDING')
            elif message.text == menu.admin_sending_btn[2]:
                bot.send_message(
                    message.chat.id, 
                    text='Рассылка отменена', 
                    reply_markup=menu.main_menu()
                )
                bot.send_message(
                    message.chat.id, 
                    text='Меню админа', 
                    reply_markup=menu.admin_menu()
                )
            else:   
                msg = bot.send_message(
                    message.chat.id, 
                    text='Не верная команда, повторите попытку', 
                    reply_markup=menu.admin_sending)



    bot.polling(none_stop=True, interval=0)

    

start_bot()
