var config = {};

config.admins = [] // id админов бота

config.mongodb = 'mongodb://c31376_mexanikrobot_bot:QiKqiXikfisep30@mongo1.c31376.h2,mongo2.c31376.h2,mongo3.c31376.h2/c31376_mexanikrobot_bot?replicaSet=MongoReplica'; // База бота MongoDB // Можно купить у @artemproger

config.qiwitoken = ''; // QIWI токен получить тут qiwi.com/api с 4 галочками

config.qiwinumber = '' // Номер киви без +

config.tokenbot = '1555112666:AAGhTz9oSxylQUWIzVmSZJGnQTx-TIy_4j4'; // Токен телеграмм бота полученный в @botfather

config.account = 'P1040816512'; // Номер payeer

config.apiPass = "KzX3F12mnrlAkJSV" ;// Секретный ключ api payeer

config.apiId = 1262222730 // id api payeer

config.enabled = true

config.trees = [
	{
		id: 0,
		name: "Механик-1уровня",
		earn: 25,
		price: 15
	},
	{
		id: 1,
		name: "Механик-2уровня",
		earn: 80,
		price: 30
	},
	{
		id: 2,
		name: "Механик-3уровня",
		earn: 100,
		price: 50
	},
	{
		id: 3,
		name: "Механик-4уровня",
		earn: 180,
		price: 100
	},
	{
		id: 4,
		name: "Механик-5уровня",
		earn: 370,
		price: 200
	},
	{
		id: 5,
		name: "Механик-6уровня",
		earn: 890,
		price: 500
	},
	{
		id: 6,
		name: "Механик-7уровня",
		earn: 1500,
		price: 1000
	},
	{
		id: 7,
		name: "Механик-8уровня",
		earn: 3000,
		price: 2000
	},
];  // цены,доходы и названия

config.startkeyboard = [
	[ "Гараж🛠️", "🎁 Подарки", "⚡ Обменник"],
	["🖥 Личный кабинет", "👥 Партнёры"],
	["👑 Комната", "📚 О боте"]
];  // Клавиатура Start

config.referal = 0.25 // Цена за реферала

config.textstart = `
✌️ <b>Привет!</b>
📝 <b>Цель игры:</b>
├─Пополняем счет 🤘
├─Покупаем автомобили
├─Собираем энергию ⚡
├─Обмениваем доход 💵
└─Получаем деньги 💹

🏝 <b>Чат</b> 👉 @End_Soft
💳 <b>Выплаты</b> 👉 @End_Soft
📢 <b>Новости</b> 👉 @End_Soft` // Текст при нажатии /start

config.pers = 'механика'

config.perss = 'механиков'

config.persss = 'механиков'

config.minwithdraw = 5 // Минимальный вывод

config.maxwithdraw = 1.50 // В сколько раз можно окупится 

config.one = 'Гараж🛠️'

config.one_one = '🛒 Магазин'

config.one_two = 'Мои автомобили '

config.two = '🎁 Подарки'

config.two_one = '🎁 Подарок № 1'

config.three = '⚡ Обменник'

config.threetextone = 'В разделе ⚡ Обменник Вы сможете обменять <b>⚡ Энерию</b> на <b>₽ рубли</b>\n\n1000 ⚡ Энергии = 1 рубль\nМинимальная сумма обмена: 1000 Энергии'

config.threetexttwo = 'Энергия'

config.threetextthree = 'Плодов'

config.three_two = '🛍️ Продать ⚡'

config.four = '🖥 Личный кабинет'

config.four_one = '📥 Пополнить'

config.four_two = '📤 Вывести'

config.four_three = '♻️ Реинвест'

config.four_four = 'Мои автомобили'

config.five = '👥 Партнёры'

config.bot = 'Mechanikribot' // Ссылка на бота без @

config.six = '👑 Комната'

config.six_one = '➕ Создать комнату'

config.six_two = '😎 ТОП Комнат'

config.six_three = '❗️ Статус битвы'

config.teplica_one = 'Комнате'

config.teplica_two = 'Комнатой'

config.teplica_three = 'Комната'

config.teplica_four = 'Комнаты'

config.teplica_five = 'Комнату'

config.teplica_six = 'Комнат'

config.admin = 'End_Soft' // Ссылка на админа без @

config.proger = 'End_Soft'

config.chat = 'End_Soft' // Ссылка на Чат без @

config.deposit = 'End_Soft' // Ссылка на канал с выплатами и пополнениями без @

config.novosti = 'End_Soft' // Ссылка на канал с новостями без @

config.startbot = '5.01.2020' // Старт бота

config.limit = 15 // Лимит персонажей

config.ogorod = 'Энергия'

config.ogorode = 'Энергии'

config.prize = 'Механик-1уровня' // Подарок при подписки

config.prizecheck = 'End_Soft'// Канал на который нужно подписатся чтоб получить подарок без

config.prizeid = 0 // id семена для подарка

module.exports = config;
