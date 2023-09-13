import sqlite3
import settings


class User():
    
    def __init__(self, user_id):
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
        user = cursor.fetchone()

        self.user_id = user[0]
        self.username = user[1]
        self.date = user[2]
        self.ref_code = user[3]
        self.who_invite = user[4]
        self.balance = float(user[5])


    def update_balance(self, value):
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        
        cursor.execute(f'UPDATE users SET balance = {float(self.balance) + float(value)} WHERE user_id = "{self.user_id}"')
        conn.commit()

        return True


    def give_money(self, bot, user_id, amount):
        if self.balance >= amount:
            self.update_balance(-amount)

            user = User(user_id)
            user.update_balance(amount)

            bot.send_message(chat_id=user_id, text=f'✅ @{self.username} перевел вам {amount} ₽')
            bot.send_message(chat_id=self.user_id, text=f'✅ Вы перевели {amount} ₽ пользователю @{user.username}')

            try:
                bot.send_message(chat_id=settings.CHAT_ID, text=f'✅ @{self.username} успешно перевел {amount} ₽ пользователю @{user.username}')
            except: print('ERROR CHAT_ID in settings.py')
        else:
            try:
                bot.send_message(chat_id=settings.CHAT_ID, text=f'❌ @{self.username} на балансе не достатачно средств')
            except: print('ERROR CHAT_ID in settings.py')
