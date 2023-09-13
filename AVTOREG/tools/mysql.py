# -*- coding: utf-8 -*-
import sqlite3
 
def connect():

	conn = sqlite3.connect('avto.db')

	cursor = conn.cursor()

	return conn, cursor





def create_tables():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_users')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_users (id,userid,balance,counry,rules,ref1,ref_earn,date_reg) VALUES  ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s')"%(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
		except:
			continue
	conn.commit()


def ugc_statistika():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_statistika')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_statistika (id,deposit_summa,summa_phones) VALUES  ('%s', '%s', '%s')"%(i[0],i[1],i[2]))
		except:
			continue
	conn.commit()

def ugc_rent_list():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_rent_list')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_rent_list (id,userid,name,rentid,phone,price,activ,data_start,data_end) VALUES  ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s')"%(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
		except:
			continue
	conn.commit()

def ugc_phones():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_phones')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_phones (id,userid,nubmer,service,sms,price,phone_id,site,date_get) VALUES  ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s')"%(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
		except:
			continue
	conn.commit()


def ugc_pays_btc():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_pays_btc')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_pays_btc (userid,text,date_pay,summa,id) VALUES  ('%s', '%s', '%s','%s', '%s')"%(i[0],i[1],i[2],i[3],i[4]))
		except:
			continue
	conn.commit()

def ugc_pays():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_pays')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_pays (id,pay_id,userid,date_pay,summa) VALUES  ('%s', '%s', '%s','%s', '%s')"%(i[0],i[1],i[2],i[3],i[4]))
		except:
			continue
	conn.commit()



def ugc_bans():
	conn, cursor = connect()
	connection = sqlite3.connect('database.sqlite3')
	q = connection.cursor()
	q = q.execute(f'SELECT * FROM ugc_bans')
	row = q.fetchall()
	for i in row:
		try:
			print(i)
			cursor.execute("INSERT INTO ugc_bans (id,userid) VALUES  ('%s', '%s')"%(i[0],i[1]))
		except:
			continue
	conn.commit()



#ugc_statistika()
#ugc_rent_list()
#ugc_phones()
#ugc_pays_btc()
#ugc_pays()
#ugc_bans()