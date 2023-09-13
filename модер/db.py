import sqlite3
con = sqlite3.connect('bot.db')
cursor = con.cursor()

def CreateUserDB():
	cursor = con.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, id INT, reputation INT, money INT)")
	con.commit()

def CreateChatDB():
	cursor = con.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS chats(chat_name TEXT, chat_id INT)") 
	con.commit()

def UpdateUserValue(val_name, new_val, id):
	for row in cursor.execute(f"SELECT {val_name} FROM users where id={id}"):
		new = row[0]+new_val
		cursor.execute(f"UPDATE users SET {val_name}={new} where id={id}")
		con.commit()

def UpdateChatValue(val_name, new_val, id):
	for row in cursor.execute(f"SELECT {val_name} FROM chats where id={id}"):
		new = row[0]+new_val
		cursor.execute(f"UPDATE chats SET {val_name}={new} where id={id}")
		con.commit()

def UpdateUserValueMinus(val_name, new_val, id):
	for row in cursor.execute(f"SELECT {val_name} FROM users where id={id}"):
		new = row[0]-new_val
		cursor.execute(f"UPDATE users SET {val_name}={new} where id={id}")
		con.commit()

def InsertUserValues(name, id):
	cursor.execute(f'INSERT INTO users VALUES ("{name}", {id}, 0, 0)')
	con.commit()

def InsertChatValues(chat_name, chat_id):
	cursor.execute(f'INSERT INTO chats VALUES ("{chat_name}", {chat_id})')
	con.commit()

def ReplaceUserValue(val_name, new_val, id):
		cursor.execute(f"UPDATE users SET {val_name}={new_val} where id={id}")
		con.commit()