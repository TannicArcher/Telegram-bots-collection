import random
import re
import time
from datetime import datetime

from aiogram.types import Message, CallbackQuery

from config import bot_name
from keyboard.main import marry_kb
from keyboard.marries import marrye_kb
from utils.logs import writelog
from utils.main.cash import get_cash, to_str
from utils.main.db import sql
from utils.main.users import User
from utils.marries import Marry


async def marry_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]

    try:
        marry = Marry(user_id=message.from_user.id)
    except:
        try:
            marry = Marry(son=message.from_user.id)
        except:
            marry = None

    user = User(id=message.from_user.id)

    if marry is not None:
        if marry.level is None or marry.level == 0:
            marry.level = 1

    if len(arg) == 0 or arg[0].lower() in ['мой', 'моя', 'моё']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        user2 = User(id=marry.user2 if message.from_user.id == marry.user1 else marry.user1)
        user1 = User(id=marry.user2 if user2.id == marry.user1 else marry.user1)

        zams = '\n'.join(f'<code>{index}</code>. {User(id=i).link} 👮🏼' for index, i in enumerate(marry.zams,
                                                                                                   start=1))
        childs = '\n'.join(f'<code>{index}</code>. {User(id=i).link} 👶' for index, i in enumerate(marry.childs,
                                                                                                   start=1) if i not
                         in marry.zams)
        lol = datetime.now() - marry.reg_date
        xd = f'{lol.days} дн.' if lol.days > 0 else f'{int(lol.total_seconds() // 3600)} час.' \
            if lol.total_seconds() > 59 else f'{int(lol.seconds)} сек.'
        text = f'💍 Ваша семья ({user1.link} & {user2.link})\n' \
               f'👤 Название: <b>{marry.name}</b>\n' \
               f'📅 Дата создания: {marry.reg_date} (<code>{xd}</code>)\n' \
               f'💰 Бюджет семьи: {to_str(marry.balance)}\n' \
               f'👑 LVL: {marry.level}\n' \
               f'👮🏼 Заместители:\n\n{zams if len(zams) > 0 else "Нету"}\n\n' \
               f'👶 Детишки в вашей семье:\n\n{childs if len(childs) > 0 else "Нету"}'
        return await message.reply(text=text, disable_web_page_preview=True,
                                   reply_markup=marrye_kb)
    elif arg[0].lower() in ['завести', 'создать', 'предложить']:
        if marry and message.from_user.id in [marry.user1, marry.user2]:
            return await message.reply('❌ У вас уже есть семья... ая-яй изменщик(ца)!')
        try:
            user2 = User(id=message.reply_to_message.from_user.id) if message.reply_to_message else User(
                username=arg[1].replace('@', ''))
        except:
            return await message.reply('❌ Ошибка. Используйте: <code>Брак создать *{ссылка}</code>')

        try:
            Marry(user_id=user2.id)
            return await message.reply(f'❌ Ошибка. У {user2.link} уже есть семья!', disable_web_page_preview=True)
        except:
            try:
                await message.bot.send_message(chat_id=user2.id,
                                               text=f'[💍] {user.link} предлагает вам жениться!',
                                               reply_markup=marry_kb(user.id, user2.id), disable_web_page_preview=True)
            except:
                return await message.reply(f'❌ {user2.link} ниразу не писал в лс боту и я к сожалению не могу '
                                           'отправить ей запрос на свадьбу!')
        return await message.reply(f'✅ Вы успешно предложили {user2.link} пожениться!\n\nЯ уведомлю вас в личке если '
                                   'он(а) согласится поэтому обязательно напишите мне что-то в лс @hineku_bot',
                                   disable_web_page_preview=True)
    elif len(arg) >= 2 and arg[0].lower() in ['дать', 'сделать'] and arg[1].lower() in ['замом', 'зама']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        try:
            user2 = User(id=message.reply_to_message.from_user.id) if message.reply_to_message else User(
                username=arg[2].replace('@', ''))
        except:
            return await message.reply('❌ Ошибка. Используйте: <code>Семья сделать замом *{ссылка}</code>')

        try:
            if user2.id in [marry.user1, marry.user2] + marry.zams:
                return await message.reply('😐 ЭТО РОДИТЕЛЬ/ЗАМ!')
            x = Marry(son=user2.id)
            if user2.id in x.childs + x.zams and x.id != marry.id:
                return await message.reply(f'❌ Ошибка. У {user2.link} уже есть семья где он (зам/ребенок)!',
                                           disable_web_page_preview=True)
            raise Exception('123')
        except:
            if user.id in [marry.user1, marry.user2]:
                marry.add_child(user_id=user2.id, status='zam')
            else:
                return await message.reply(f'❌ Вы не родитель!')

        await message.reply(f'✅ Вы успешно сделали замом {user2.link}', disable_web_page_preview=True)
        await writelog(message.from_user.id, f'Зам семьи {user2.link}')
        return

    elif len(arg) >= 2 and arg[1].lower() == 'зама' and arg[0].lower() in ['убрать', 'снять',
                                                                           'удалить']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        if message.from_user.id in [marry.user1, marry.user2]:
            try:
                user2 = User(id=message.reply_to_message.from_user.id) if message.reply_to_message else User(
                    username=arg[2].replace('@', ''))
            except:
                return await message.reply('❌ Ошибка. Используйте: <code>Семья убрать зама *{ссылка}</code>')
            if user2.id in [marry.user1, marry.user2]:
                return await message.reply('❌ Это папа или мама!')
            elif user2.id not in marry.zams:
                return await message.reply('😐 Это не зам')
            marry.del_child(user2.id, 'zams')
            await message.reply(f'✅ Вы успешно забрали зама у {user2.link}',
                                disable_web_page_preview=True)
            await writelog(message.from_user.id, f'Зам забрать {user2.link}')
            return
        else:
            return await message.reply('👶 Шкет, ты не можешь снять другого зама!')

    elif arg[0].lower() in ['усыновить', 'приютить', 'удочерить', 'взять']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        try:
            user2 = User(id=message.reply_to_message.from_user.id) if message.reply_to_message else User(
                username=arg[1].replace('@', ''))
        except:
            return await message.reply('❌ Ошибка. Используйте: <code>Семья приютить *{ссылка}</code>')

        try:
            if user2.id in [marry.user1, marry.user2]:
                raise Exception('123')
            Marry(son=user2.id)
            return await message.reply(f'❌ Ошибка. У {user2.link} уже есть родители!', disable_web_page_preview=True)
        except:
            if user.id in [marry.user1, marry.user2] + marry.zams:
                marry.add_child(user_id=user2.id)
            else:
                return await message.reply(f'❌ Вы не родитель!')

        await message.reply(f'✅ Вы успешно приютили {user2.link}', disable_web_page_preview=True)
        await writelog(message.from_user.id, f'Приючение {user2.link}')
        return

    elif arg[0].lower() in ['выйти', 'разорвать', 'удалить']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        if message.from_user.id in [marry.user1, marry.user2]:
            marry.delete()
            await message.reply('✅ Вы успешно удалили семью! Мне очень жаль :(')
            await writelog(message.from_user.id, f'Удаление семьи')
            return
        else:
            marry.del_child(message.from_user.id)
            marry.del_child(message.from_user.id, 'zam')
            await message.reply('✅ Вы успешно вышли с семьи! Мне очень жаль :(')
            await writelog(message.from_user.id, f'Выход из семьи')
            return

    elif arg[0].lower() in ['выгнать', 'разсыновить', 'раздочерить']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        if message.from_user.id in [marry.user1, marry.user2] + marry.zams:
            try:
                user2 = User(id=message.reply_to_message.from_user.id) if message.reply_to_message else User(
                    username=arg[1].replace('@', ''))
            except:
                return await message.reply('❌ Ошибка. Используйте: <code>Семья выгнать *{ссылка}</code>')
            if user2.id in [marry.user1, marry.user2] + marry.zams:
                return await message.reply('❌ Это папа или мама, или зам!')
            marry.del_child(user2.id)
            await message.reply(f'✅ Вы успешно выгнали {user2.link} из своей семьи',
                                disable_web_page_preview=True)
            await writelog(message.from_user.id, f'Выгнание {user2.link} из семьи')
            return
        else:
            return await message.reply('👶 Шкет, ты не можешь выгнать своего брата/сестру!')
    elif arg[0].lower() in ['снять', 'вывести', 'взять']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')
        if user.id not in [marry.user1, marry.user2] + marry.zams:
            return await message.reply('❌ Вы не родитель/зам, не можете снять бабки с бюджета семьи!')

        summ = marry.balance
        try:
            summ = get_cash(arg[1])
        except:
            pass

        if summ <= 0:
            return await message.reply('❌ Минимум $1')

        elif summ > marry.balance:
            return await message.reply('❌ Недостаточно средств на счету семьи!')

        sql.executescript(f'UPDATE users SET balance = balance + {summ} WHERE id = {message.from_user.id};\n'
                          f'UPDATE marries SET balance = balance - {summ} WHERE id = {marry.id}',
                          True, False)

        await message.reply(f'✅ Вы успешно сняли {to_str(summ)} с бюджета семьи!')
        await writelog(message.from_user.id, f'Снятие {to_str(summ)} с бюджета семьи')
        return
    elif arg[0].lower() in ['положить', 'вложить', 'пополнить', 'дать']:
        if marry is None:
            return await message.reply('❌ У вас нет семьи :(')

        summ = user.balance
        try:
            summ = get_cash(arg[1])
        except:
            pass

        if summ <= 0:
            return await message.reply('❌ Минимум $1')

        elif summ > user.balance:
            return await message.reply('❌ Недостаточно средств на руках!')

        sql.executescript(f'UPDATE users SET balance = balance - {summ} WHERE id = {message.from_user.id};\n'
                          f'UPDATE marries SET balance = balance + {summ} WHERE id = {marry.id}',
                          True, False)

        await message.reply(f'✅ Вы успешно пополнили бюджет семьи на +{to_str(summ)}')
        await writelog(message.from_user.id, f'Пополнение {to_str(summ)} в бюджет семьи')
        return
    elif arg[0].lower() in ['награда', 'вознаграждение', 'награждение']:
        if marry.last is not None and (time.time() - marry.last) < 3600:
            return await message.reply('⌚ Вы недавно забирали награду')

        marry.editmany(last=time.time(),
                       balance=marry.balance + 10000 * marry.level)
        await message.reply(f'🎄 В бюджет семьи было начислено +{to_str(10000 * marry.level)}')
        await writelog(message.from_user.id, f'Награда в бюджет семьи')
        return
    elif arg[0].lower() in ['секс', 'трахать', 'трахаться', 'траханье']:
        if not marry:
            return await message.reply('❌ У вас нет семьи :(')
        if marry.last_sex is not None and (time.time() - marry.last_sex) < 3600:
            return await message.reply('⌚ Вы недавно занимались этим делом!')
        elif user.id not in [marry.user1, marry.user2] + marry.zams:
            return await message.reply('🍁 Шкет! Ты не можешь трахаца с родителем.')

        summ = random.randint(5000, 25000 * marry.level)

        marry.editmany(last_sex=time.time(),
                       balance=marry.balance + summ)

        user2 = User(id=marry.user2 if message.from_user.id == marry.user1 else marry.user1)

        await message.reply(f'🎄 Вы занялись сэксом с {user2.link} и в бюджет семьи было начислено '
                            f'+{to_str(summ)}', disable_web_page_preview=True)
        await writelog(message.from_user.id, f'Cекс с {user2.link}')
        return
    elif arg[0].lower() in ['улучш', 'улучшение', 'улучшить',
                            'буст', 'апргейд', 'апдейт']:
        if not marry:
            return await message.reply('❌ У вас нет семьи :(')

        price = 1000000 * (marry.level + 1)
        if user.balance < price:
            return await message.reply(f'💲 Недостаточно денег на руках для улучшения семьи. Нужно: {to_str(price)}')

        query = f'UPDATE users SET balance = balance - {price} WHERE id = {user.id};\n' \
                f'UPDATE marries SET level = level + 1 WHERE id = {marry.id};'
        sql.executescript(query=query, commit=True, fetch=False)

        return await message.reply(f'✅ Вы улучшили уровень семьи на +1, текущий уровень: {marry.level + 1}')
    elif arg[0].lower() in ['назвать', 'переименовать', 'ник', 'нейм',
                            'название']:
        if not marry:
            return await message.reply('❌ У вас нет семьи :(')

        if marry.level < 3:
            return await message.reply('👑 Нужен 4 лвл чтобы менять название семьи!')

        try:
            name = re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', arg[1])
        except:
            return await message.reply('❌ Используйте: <code>Брак назвать {название}</code>')
        if len(name) < 4 or len(name) > 16:
            return await message.reply('❌ Длина больше 16 или меньше 4. Запрещены символы.')

        marry.edit('name', name)

        return await message.reply(f'✅ Вы успешно изменили название семьи на: <b>{name}</b>')

    else:
        return await message.reply('❌ Ошибка. Используйте документацию чтобы узнать команды!')


async def marry_call_handler(call: CallbackQuery):
    user1 = int(call.data.split('_')[1])
    try:
        Marry(user_id=user1)
        await call.answer('❌ Пользователь уже поженился')
        return await call.message.delete()
    except:
        pass
    try:
        Marry(user_id=call.from_user.id)
        await call.answer('❌ Пользователь уже поженился')
        return await call.message.delete()
    except:
        pass
    try:
        await call.bot.send_message(chat_id=user1,
                                    text=f'Ура, ваша вторая половинка которой'
                                         f' вы предлагали пожениться приняла запрос на свадьбу!')
    except:
        pass
    Marry.create(user1=user1, user2=call.from_user.id)
    await call.answer('Брак зарегистрирован!')
    try:
        await call.message.delete()
    except:
        pass
    await writelog(call.from_user.id, f'Свадьба с {user1}')
    return
