import telebot
from telebot import types
import sqlite3
import requests
import config
import json
import pymysql

def connect():

	con = pymysql.connect(
		host='.154..82',
		user='',
		password='',
		database=''
	)

	cursor = con.cursor()

	return con, cursor


def main():
	main_menu = telebot.types.ReplyKeyboardMarkup(True)
	main_menu.row('👮‍♀️ Миксер','📖 Информация')
	main_menu.row('📖 Статистика')
	main_menu.row('📱Самые Лучшие Номера📲')
	return main_menu
