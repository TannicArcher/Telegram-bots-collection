from telethon import TelegramClient, events, sync
import re
import datetime
import time
import asyncio
import requests
import sqlite3


def check_btc():
    while True:
        try:
            time.sleep(3)

            conn = sqlite3.connect('btc.db')
            cursor = conn.cursor()

            cursor.execute(f'SELECT * FROM payouts_step_0')
            payouts_step_0 = cursor.fetchall()

            if len(payouts_step_0) == 0 :
                cursor.execute(f'SELECT * FROM btc_list')
                btc_list = cursor.fetchall()

                if len(btc_list) == 0:
                    pass
                else:
                    cursor.execute(f'INSERT INTO payouts_step_0 VALUES ("{btc_list[0][0]}", "{btc_list[0][1]}", "{time.time()}")')
                    conn.commit()

                    asyncio.set_event_loop(asyncio.new_event_loop())
                    asyncio.run(btc(btc_list[0][1]))

                    print('check_btc CLOSE')
            else:
                if time.time() - float(payouts_step_0[0][2]) > 30:
                    asyncio.set_event_loop(asyncio.new_event_loop())
                    asyncio.run(btc(payouts_step_0[0][1]))

        except Exception as e:
            print('btc...')


def btc(code):
    api_id = '1813245'
    api_hash = '834dfd07290d38ef1913a1e5c4915eea'

    client = TelegramClient(session='CheckBt', api_id=api_id, api_hash=api_hash, app_version='Version alpha', device_model='Test models', system_version='Android 999')
    client.start()

    client.send_message('me', 'start')

    client.send_message('BTC_CHANGE_BOT', '/start ' + code)

    conn = sqlite3.connect('btc.db')
    cursor = conn.cursor()

    @client.on(events.NewMessage())
    async def handler(event):
        msg = event.message.message

        if msg == 'Упс, кажется, данный чек успел обналичить кто-то другой 😟':

            cursor.execute(f'SELECT * FROM payouts_step_0')
            row = cursor.fetchall()

            if len(row) > 0:
                    cursor.execute(f'INSERT INTO payouts VALUES ("{row[0][0]}", "0", "{row[0][1]}")')
                    conn.commit()

                    cursor.execute(f'DELETE FROM payouts_step_0 WHERE user_id = "{row[0][0]}"')
                    conn.commit()

                    cursor.execute(f'DELETE FROM btc_list WHERE user_id = "{row[0][0]}"')
                    conn.commit()

                    await client.disconnect()

            return 'BAD'
        
        if 'Вы получили' in msg:
            cursor.execute(f'SELECT * FROM payouts_step_0')
            row = cursor.fetchall()

            if len(row) > 0:

                x2 = re.findall('получили \d+ BTC|получили \d.\d+ BTC', msg)[0]
                x3 = re.findall('\d[.]\d+|\d+', msg)[0]

                rub = float('{:.2}'.format(float(x3)*curs()))  
                
                try:
                    cursor.execute(f'INSERT INTO deposit_logs VALUES ("{row[0][0]}", "banker", "{rub}", "{datetime.datetime.now()}")')
                    conn.commit()
                except:
                    pass

                cursor.execute(f'INSERT INTO payouts VALUES ("{row[0][0]}", "{rub}", "{row[0][1]}")')
                conn.commit()

                cursor.execute(f'DELETE FROM payouts_step_0 WHERE user_id = "{row[0][0]}"')
                conn.commit()

                cursor.execute(f'DELETE FROM btc_list WHERE user_id = "{row[0][0]}"')
                conn.commit()

                await client.disconnect()

    client.run_until_disconnected()


def add_to_queue(user_id, url):
    code = re.findall(r'c_\S+', url)[0]

    conn = sqlite3.connect('btc.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM btc_list where user_id = "{user_id}"')
    check = cursor.fetchall()

    if len(check) > 0:
        return f'Вы уже отправили чек на обработку: {check[0][1]}'
    else:
        cursor.execute(f'INSERT INTO btc_list VALUES ("{user_id}", "{code}")')
        conn.commit()

        cursor.execute(f'SELECT * FROM btc_list')
        btc_list = cursor.fetchall()
        
        time = len(btc_list) * 10

        return f'🔍 Ожидайте, скоро бот проверит ваш чек: {code}\n\n⏱ Примерное время ожидание: {time} секунд'
        

def curs():
    response = requests.get(
            'https://blockchain.info/ticker',
        ) 

    return float(response.json()['RUB']['15m'])
