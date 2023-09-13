#ID BOT
import logging
from aiogram import Bot, Dispatcher, executor, types


import config
from config import token


bot = Bot(token=config.token)
dp = Dispatcher(bot=bot)



logging.basicConfig(level=logging.INFO)

@dp.message_handler(content_types=['text'], text=['/start', '/start@getidarcher_bot'])
async def start_cmd2(message):
        	  await bot.send_message(message.chat.id, f'''
<b>Привет! Этот бот создан чтобы вы узнали какой ID у чата, пользователя, у себя.</b>

<b>Команды:</b>
  <code>/me</code> • <i>твой ID</i>
  
  <code>/id</code> • <i>ID левого человека (работает ответом на сообщение)</i>
  
  <code>/chat</code> • <i>ID чата (нужно добавить бота в чат)</i>
  
  <b>Также в боте поддерживаются префиксы :</b> <code>!</code>  <code>.</code>''', parse_mode='HTML')


#ТВОЙ ID
@dp.message_handler(commands=["me"], commands_prefix='!./')
async def id(message):
	user_id = message.from_user.id
	await message.reply(f"<b>Твой ID:</b> <code>{user_id}</code>\n <b>Нажмите на ID чтобы скопировать.</b> \nFrom @archerdeveloping", parse_mode='HTML')
	


#ID ЛЕВОГО ЧЕЛА (надо добавить бота в группу и писать ответом на сообщение того чувака у которого вы хотите узнать ID)
@dp.message_handler(commands=["id"], commands_prefix='!./')
async def id(message):
	user_id = message.reply_to_message.from_user.id
	if message.reply_to_message:
		await message.reply(f"<b>ID участника:</b> <code>{user_id}</code>\n <b>Нажмите на ID чтобы скопировать.</b>", parse_mode='html')	
	if not message.reply_to_message:
		await message.reply(f"<b>Команда</b> <code>/id</code> <b>работает только ответом на сообщение!</b>", parse_mode='HTML')
		

#ID чата (пример: -1000000000000)
#Также надо добавить бота в чат, работать должно так и с публичными так и приватными.
#Просто пишем в группу "/chat"
@dp.message_handler(commands=["chat"], commands_prefix='!./')
async def id(message):
	user_id = message.chat.id
	await message.reply(f"<b>ID этого притона:</b> <code>{user_id}</code>\n <b>Нажмите на ID чтобы скопировать.</b>", parse_mode='HTML')
	




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
