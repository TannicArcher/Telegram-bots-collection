        if message.text.startswith("Депозит положить"):
          	chat_id = message.chat.id
          	user_id = message.from_user.id
          	user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
          	user_name = (user_name[0])
          	reply = message.from_user.id
          	get = cursor.execute("SELECT last_depozit FROM times WHERE user_id=?", (user_id,)).fetchall()
          	last_depozit = f'{int(get[0][0])}'       
          	depozit_p = float(message.text.split()[2])
          	timedepozit = time.time() - float(last_depozit)
          	period = 172800
          	balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
          	balance = round(int(balance[0]))
          	depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
          	depozit = round(int(depozit[0]))
          	c = Decimal(depozit_p)
          	c2 = round(c)
          	c2 = '{:,}'.format(c2)
          	win = ['🙂', '😋', '😄', '🤑', '😃']
          	rwin = random.choice(win)
          	loser = ['😔', '😕', '😣', '😞', '😢']
          	rloser = random.choice(loser)
          	if timedepozit < period:
          		await message.reply(f'Нет! Под депозит можно положить каждые 2 дня! Пожалуйста подождите!')
          	if timedepozit > period:
          	   if c > 0:
          	      if balance >= c:
          	      	await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, вы успешно положили под депозит: {c2}$\nМожно забрать через 2 дня! {rwin}', parse_mode='html')
          	      	cursor.execute(f'UPDATE users SET balance = {balance - depozit_p} WHERE user_id = "{user_id}"')
          	      	cursor.execute(f'UPDATE users SET depozit = {depozit + c} WHERE user_id = "{user_id}"')
          	      	cursor.execute(f'UPDATE times SET last_depozit = ? WHERE user_id=?', (time.time(), user_id,))
          	      	connect.commit()    
   
          	   elif int(balance) < int(c):
          	      await bot.send_message(message.chat.id, f'💰 | <a href="tg://user?id={reply}">{user_name}</a>, недостаточно средств! {rloser}', parse_mode='html')

          	if c <= 0:
          	   await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, нельзя положить под депозит отрицательное число! {rloser}', parse_mode='html')
          	   
        if message.text.startswith("депозит положить"):
          	chat_id = message.chat.id
          	user_id = message.from_user.id
          	user_name = cursor.execute("SELECT user_name from users where user_id = ?",(message.from_user.id,)).fetchone()
          	user_name = (user_name[0])
          	reply = message.from_user.id
          	get = cursor.execute("SELECT last_depozit FROM times WHERE user_id=?", (user_id,)).fetchall()
          	last_depozit = f'{int(get[0][0])}'       
          	depozit_p = float(message.text.split()[2])
          	timedepozit = time.time() - float(last_depozit)
          	period = 172800
          	balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
          	balance = round(int(balance[0]))
          	depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
          	depozit = round(int(depozit[0]))
          	c = Decimal(depozit_p)
          	c2 = round(c)
          	c2 = '{:,}'.format(c2)
          	win = ['🙂', '😋', '😄', '🤑', '😃']
          	rwin = random.choice(win)
          	loser = ['😔', '😕', '😣', '😞', '😢']
          	rloser = random.choice(loser)
          	if timedepozit < period:
          		await message.reply(f'Нет! Под депозит можно положить каждые 2 дня! Пожалуйста подождите!')
          	if timedepozit > period:
          	   if c > 0:
          	      if balance >= c:
          	      	await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, вы успешно положили под депозит: {c2}$\nМожно забрать через 2 дня! {rwin}', parse_mode='html')
          	      	cursor.execute(f'UPDATE users SET balance = {balance - depozit_p} WHERE user_id = "{user_id}"')
          	      	cursor.execute(f'UPDATE users SET depozit = {depozit + c} WHERE user_id = "{user_id}"')
          	      	cursor.execute(f'UPDATE times SET last_depozit = ? WHERE user_id=?', (time.time(), user_id,))
          	      	connect.commit()    
   
          	   elif int(balance) < int(c):
          	      await bot.send_message(message.chat.id, f'💰 | <a href="tg://user?id={reply}">{user_name}</a>, недостаточно средств! {rloser}', parse_mode='html')

          	if c <= 0:
          	   await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, нельзя положить под депозит отрицательное число! {rloser}', parse_mode='html')
    
        if message.text.startswith("депозит снять"):
          	message = message
          	chat_id = message.chat.id
          	user_id = message.from_user.id
          	name = message.from_user.last_name 
          	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
          	user_name = str(user_name[0])
          	reply = message.from_user.id
          	depozit_s = float(message.text.split()[2])
          	balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
          	balance = round(int(balance[0]))
          	depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
          	depozit = round(int(depozit[0]))
          	c = Decimal(depozit_s)
          	c2 = round(c)
          	c2 = '{:,}'.format(c2)
          	win = ['🙂', '😋', '😄', '🤑', '😃']
          	rwin = random.choice(win)
          	loser = ['😔', '😕', '😣', '😞', '😢']
          	rloser = random.choice(loser)
          	period = 172800
          	get = cursor.execute("SELECT last_depozit FROM times WHERE user_id = ?", (message.from_user.id,)).fetchone()
          	last_stavka = f'{int(get[0])}'
          	stavkatime = time.time() - float(last_stavka)
          	if stavkatime < period:
          		await message.reply(f"Нет! Ты можешь снять с депозита через 2 дня после того как ты положил её в депозит!{rloser}")
          	if stavkatime > period:
          			if c > 0:
          				if depozit > c:
          					await message.reply(f'Ты успешно снял свои деньги с депозита! И да, твоя сумма увеличена на 10%.')
          					cursor.execute(f'UPDATE users SET depozit = {depozit - depozit_s} WHERE user_id = "{user_id}"')       				
          					cursor.execute(f'UPDATE users SET balance = {balance + depozit_s * 1.10} WHERE user_id = "{user_id}"')
          					connect.commit()
          					return
          				if int(depozit) < int(c):
          					await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, недостаточно средств под депозитом! {rloser}', parse_mode='html')

          				if c <= 0:
          				 await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, нельзя снять с депозита отрицательное число! {rloser}', parse_mode='html')
          				 
        if message.text.startswith("Депозит снять"):
          	message = message
          	chat_id = message.chat.id
          	user_id = message.from_user.id
          	name = message.from_user.last_name 
          	user_name = cursor.execute("SELECT user_name from users where user_id = ?", (message.from_user.id,)).fetchone()
          	user_name = str(user_name[0])
          	reply = message.from_user.id
          	depozit_s = float(message.text.split()[2])
          	balance = cursor.execute("SELECT balance from users where user_id = ?", (message.from_user.id,)).fetchone()
          	balance = round(int(balance[0]))
          	depozit = cursor.execute("SELECT depozit from users where user_id = ?", (message.from_user.id,)).fetchone()
          	depozit = round(int(depozit[0]))
          	c = Decimal(depozit_s)
          	c2 = round(c)
          	c2 = '{:,}'.format(c2)
          	win = ['🙂', '😋', '😄', '🤑', '😃']
          	rwin = random.choice(win)
          	loser = ['😔', '😕', '😣', '😞', '😢']
          	rloser = random.choice(loser)
          	period = 172800
          	get = cursor.execute("SELECT last_depozit FROM times WHERE user_id = ?", (message.from_user.id,)).fetchone()
          	last_stavka = f'{str(get[0])}'
          	stavkatime = time.time() - float(last_stavka)
          	if stavkatime < period:
          		await message.reply(f"Нет! Ты можешь снять с депозита через 2 дня после того как ты положил её в депозит!{rloser}")
          	if stavkatime > period:
          			if c > 0:
          				if depozit > c:
          					await message.reply(f'Ты успешно снял свои деньги с депозита! И да, твоя сумма увеличена на 10%.')
          					cursor.execute(f'UPDATE users SET depozit = {depozit - depozit_s} WHERE user_id = "{user_id}"')       				
          					cursor.execute(f'UPDATE users SET balance = {balance + depozit_s * 1.10} WHERE user_id = "{user_id}"')
          					connect.commit()
          					return
          				if int(depozit) < int(c):
          					await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, недостаточно средств под депозитом! {rloser}', parse_mode='html')

          				if c <= 0:
          				 await bot.send_message(message.chat.id, f'<a href="tg://user?id={reply}">{user_name}</a>, нельзя снять с депозита отрицательное число! {rloser}', parse_mode='html')
          				 
          				 
          				#####по вопросам можешь обращаться.))