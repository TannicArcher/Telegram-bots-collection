let news		=		require("./news");

let sponsor		=		require("./sponsor");

let more_project		=		require("./more_project");

const mongo = require("mongoose");
mongo.connect("");

const User = mongo.model("User", {
	id: Number,
	partner: Number,
	menu: String,
	adminmenu: String,
	regDate: String,
  data: String,
  name: String,
  verify: Boolean
});

const admins =	[];

const Telegram = require("node-telegram-bot-api");
const bot = new Telegram("", { polling: true });

const keyboards = {
	main: [
		["🔎 Поиск"],
		["🗄 Кабинет", "📰 Газета", "📃 Правила"],
		["📊 Статистика", "📢 Реклама"]
	],
	main_search: [
		["🚫 Остановить поиск"],
		["🗄 Кабинет", "📰 Газета", "📃 Правила"],
		["📊 Статистика", "📢 Реклама"]
],
	main_in_dialog: [
		["🚫 Остановить диалог"],
		["🗄 Кабинет", "📃 Газета", "📋 Правила"],
		["📊 Статистика", "📢 Реклама"]
	],
	newspaper: [
	  ["📌 Об'явлення"],
	  ["🔋 Спонсори", "🛡 Другие проекти"],
	  ["⛔️ Отмена"]
	],
	cancel: [
		["⛔️ Отмена"]
	],
	admin: [
		["📬 Рассылка", "📝 Редактор Газети"],
		["🔐 Статус"],
		["🚪 Начало"]
	],
	admin_newspaper: [
	  ["⚙ 📌", "⚙ 🔋", "⚙ 🛡"],
	  ["⛔️ Отмена"]
  ]
}

let queue = [];

bot.on("message", async (message) => {
	message.send = (text, params) => bot.sendMessage(message.chat.id, text, params);

	let $user = await User.findOne({ id: message.from.id });
	if( !$user ) {
		let user = new User({
			id: message.from.id,
			partner: 0,
			menu: "",
			adminmenu: "",
			verify: false
		});

		await user.save();
		return message.send(`🕹 Меню`,
	{
		 reply_markup: {
				keyboard: keyboards.main,
				resize_keyboard: true
			}
		});
	}

	message.user = await User.findOne({ id: message.from.id });
	if(message.text.startsWith("/start")) {
		return message.send(`🕹 Меню:`, {
			reply_markup: {
				keyboard: message.user.partner ? keyboards.main_in_dialog : queue.indexOf(message.from.id) === -1 ? keyboards.main : keyboards.main_search,
				resize_keyboard: true
			}
		});
	}

	message.user = await User.findOne({ id: message.from.id });

	if(message.text === "⛔️ Отмена" || message.text === "🚪 Начало") {
		await message.user.set("menu", "");
		await message.user.set("adminmenu", "");

		return message.send(`❌ Операция отменена`, {
			reply_markup: {
				keyboard: keyboards.main,
				resize_keyboard: true
			}
		});
	}

	if(admins.indexOf(message.from.id) !== -1) {
		if(message.user.menu.startsWith("auditory")) {
			let users		=		await User.find();
			let total		=		users.length * Number(message.user.menu.split("auditory")[1]);

			for (let i = 0; i < total; i++) {
				if(message.photo) {
					let file_id = message.photo[message.photo.length - 1].file_id;
					let params = {
						caption: message.caption,
						parse_mode: "HTML",
						disable_web_page_preview: true
					}

					if(message.caption.match(/(?:кнопка)\s(.*)\s-\s(.*)/i)) {
						let [ msgText, label, url ] = message.caption.match(/(?:кнопка)\s(.*)\s-\s(.*)/i);
						params.reply_markup = {
							inline_keyboard: [
								[{ text: label, url: url }]
							]
						}

						params.caption = params.caption.replace(/(кнопка)\s(.*)\s-\s(.*)/i, "");
					}

					bot.sendPhoto(users[i].id, file_id, params);
				}

				if(!message.photo) {
					let params = {
						parse_mode: "HTML",
						disable_web_page_preview: true
					}

					if(message.text.match(/(?:кнопка)\s(.*)\s-\s(.*)/i)) {
						let [ msgText, label, url ] = message.text.match(/(?:кнопка)\s(.*)\s-\s(.*)/i);
						params.reply_markup = {
							inline_keyboard: [
								[{ text: label, url: url }]
							]
						}
					}

					bot.sendMessage(users[i].id, message.text.replace(/(кнопка)\s(.*)\s-\s(.*)/i, ""), params);
				}
			}

			await message.user.set("menu", "");
			await message.send("✳️ Рассылка успешно завершена", {
				reply_markup: {
					keyboard: keyboards.admin,
					resize_keyboard: true
				}
			});
		}

		if(message.user.menu === "selectAuditory") {
			await message.user.set("menu", "auditory" + Number(message.text));
			return message.send(`📃 Введите текст рассылки
			
📺 Можно прикрепить изображение`, {
				reply_markup: {
					keyboard: keyboards.cancel,
					resize_keyboard: true
				}
			});
		}
		if(message.text === "📬 Рассылка") {
			await message.user.set("menu", "selectAuditory");
			return message.send(`👤 Выберите аудиторию

📉 0.25	—	25%
📉 0.50	—	50%
📉
📈0.75	—	75%
1		—	100%`, {
				reply_markup: {
					keyboard: [["0.25", "0.50"], ["0.75", "1"], ["⛔️ Отмена"]],
					resize_keyboard: true
				}
			});
		}	
	}

	if(message.text === "🔎 Поиск") {
		if(message.user.partner) return message.send(`💬 Вы уже в диалоге!`, {
			reply_markup: {
				keyboard: keyboards.main_in_dialog,
				resize_keyboard: true
			}
		});

		if(queue.indexOf(message.from.id) !== -1) return message.send(`🕒 Вы уже в поиске`, {
			reply_markup: {
				keyboard: keyboards.main_search,
				resize_keyboard: true
			}
		});

		if(queue[0]) {
			queue.push(message.from.id);
			let partner = await User.findOne({ id: queue[0] });

			await partner.set("partner", queue[1]);
			await message.user.set("partner", queue[0]);

			bot.sendMessage(queue[0], "✳️ Собеседник найден, общайтесь!", {
				reply_markup: {
					keyboard: keyboards.main_in_dialog,
					resize_keyboard: true
				}
			});

			message.send("✳ ️Собеседник найден, общайтесь!", {
				reply_markup: {
					keyboard: keyboards.main_in_dialog,
					resize_keyboard: true
				}
			});

			queue = [];
		} else {
			queue.push(message.from.id);
			return message.send(`🕒 Вы добавлены в очередь поиска, ожидайте собеседника!`, {
				reply_markup: {
					keyboard: keyboards.main_search,
					resize_keyboard: true
				}
			});
		}
	}

	if(message.text === "🚫 Остановить поиск") {
		if(queue.indexOf(message.from.id) === -1) return message.send(`❌ Вы не в очереди!`, {
			reply_markup: {
				keyboard: message.user.partner ? keyboards.main_in_dialog : keyboards.main,
				resize_keyboard: true
			}
		});

		queue = [];
		return message.send(`❌ Вы вышли из очереди!`, {
			reply_markup: {
				keyboard: keyboards.main,
				resize_keyboard: true
			}
		});
	}
	
	if(admins.indexOf(message.from.id) !== -1) {
	  if(message.text === "📝 Редактор Газети") {
	    return message.send(`📝 <b> Редактор Газети: </b>`, 
	    {
	    parse_mode: "HTML",
			reply_markup: {
				keyboard: keyboards.admin_newspaper,
				resize_keyboard: true
			 }
		  });
	  }
 	}
	
	
 	if(admins.indexOf(message.from.id) !== -1) {
	  if(message.text === "/admin") {
	    return message.send(`🛠 <b> Админ панель: </b>`, 
	    {
	    parse_mode: "HTML",
			reply_markup: {
				keyboard: keyboards.admin,
				resize_keyboard: true
			 }
		  });
	  }
 	}
	
	if(message.text === "🚫 Остановить диалог") {
		if(!message.user.partner) return message.send(`❌ Вы не в диалоге!`, {
			reply_markup: {
				keyboard: queue.indexOf(message.from.id) !== -1 ? keyboards.main_search : keyboards.main,
				resize_keyboard: true
			}
		});

		let partner = await User.findOne({ partner: message.from.id });
		
		await partner.set("partner", 0);
		await message.user.set("partner", 0);

		bot.sendMessage(partner.id, "❌ Ваш собеседник отключился!", {
			reply_markup: {
				keyboard: keyboards.main,
				resize_keyboard: true
			}
		});

		message.send(`❌ Вы отключились`, {
			reply_markup: {
				keyboard: keyboards.main,
				resize_keyboard: true
			}
		});
	}

  if(message.text === "📰 Газета") {
		return message.send(`<b> 🗞 Выберите пункт газеты: </b>`, {
			parse_mode: "HTML",
			reply_markup: {
				keyboard: keyboards.newspaper,
				resize_keyboard: true
			}
		});
	}

	if(message.text === "📊 Статистика") {
		return message.send(
			`➖➖ 📊 <b>Статистика бота</b > ➖➖`
			+ `\n`
			+ `👤 Пользователей в боте: <b>${ await User.countDocuments() }</b>`
			+ `\n`
			+ `🕐 Старт бота: <b>31
			08.2020</b>`,
			{ parse_mode: "HTML", }
			);
	}

  if(message.text === "📌 Об'явлення")
   { 
  return message.send(news, {
  parse_mode: "HTML"
  });
   }
   
  if(message.text === "🔋 Спонсори")
   { 
  return message.send(sponsor, {
  parse_mode: "HTML"
  });
   }
  
  if(message.text === "🛡 Другие проекти")
   { 
  return message.send(more_project, {
  parse_mode: "HTML"
  });
   }

  if(admins.indexOf(message.from.id) !== -1) {
  if(message.text === "⚙ 📌") {
			await message.user.set("menu", "news");
			return message.send(`✏️ <b>Введите текст для 📌 Об'явлення</b>`, 
			{ parse_mode: "HTML"} ,
			{				
			  reply_markup: {
					keyboard: keyboards.cancel,
					resize_keyboard: true
				}
			});
		}
  }
	
	if(message.user.menu === "news") {
			require("fs").writeFileSync("./news.json", JSON.stringify(message.text));
			news = message.text;

			await message.user.set("menu", "");
			return message.send(`✳️ <b>Успешно</b>`, {
			  parse_mode: "HTML",
				reply_markup: {
					keyboard: keyboards.admin,
					resize_keyboard: true
				}
			});
		}
		
	if(admins.indexOf(message.from.id) !== -1) {
  if(message.text === "⚙ 🔋") {
			await message.user.set("menu", "sponsor");
			return message.send(`✏️ <b>Введите текст для 🔋 Спонсори</b>`, 
			{ parse_mode: "HTML"} ,
			{				
			  reply_markup: {
					keyboard: keyboards.cancel,
					resize_keyboard: true
				}
			});
		}
  }
	
	if(message.user.menu === "sponsor") {
			require("fs").writeFileSync("./sponsor.json", JSON.stringify(message.text));
			sponsor = message.text;

			await message.user.set("menu", "");
			return message.send(`✳️ <b>Успешно</b>`, {
			  parse_mode: "HTML",
				reply_markup: {
					keyboard: keyboards.admin,
					resize_keyboard: true
				}
			});
	}

  if(admins.indexOf(message.from.id) !== -1) {
  if(message.text === "⚙ 🛡") {
			await message.user.set("menu", "more_project");
			return message.send(`✏️ <b>Введите текст для 📌 Об'явлення</b>`, 
			{ parse_mode: "HTML"} ,
			{				
			  reply_markup: {
					keyboard: keyboards.cancel,
					resize_keyboard: true
				}
			});
		}
  }
	
	if(message.user.menu === "more_project") {
			require("fs").writeFileSync("./more_project.json", JSON.stringify(message.text));
			more_project = message.text;

			await message.user.set("menu", "");
			return message.send(`✳️ <b>Успешно</b>`, {
			  parse_mode: "HTML",
				reply_markup: {
					keyboard: keyboards.admin,
					resize_keyboard: true
				}
			});
		}

  if(admins.indexOf(message.from.id) !== -1) {
		if(message.user.menu === "enterVerify") {
			message.text		=		Math.floor(Number(message.text));
			if(!message.text) return message.send(`🆔 <b>Введите айди:</b>`,
			{ parse_mode: "HTML", });

			let user			=		await User.findOne({ id: message.text });
			if(!user) return message.send(`❎ <b>Пользователь не найден</b>`,
			{ parse_mode: "HTML", });

			if(user.verify) {
				await user.set("verify", false);
				await message.user.set("menu", "");

				return message.send(`❌ <b> Вы удалили верификацию</b>`, {
					parse_mode: "HTML",
					reply_markup: {
						keyboard: keyboards.admin,
						resize_keyboard: true
					}
				});
			} else {
				await user.set("verify", true);
				await message.user.set("menu", "");

				return message.send(`✳️ <b>Вы выдали верификацию</b>`, {
				  parse_mode: "HTML",
					reply_markup: {
						keyboard: keyboards.admin,
						resize_keyboard: true
					}
				});
			}
	}

  if(message.text === "🔐 Статус") {
			await message.user.set("menu", "enterVerify");
			return message.send(`🆔 <b>Введите айди пользователя:</b>`,
			{
			parse_mode: "HTML",
				reply_markup: {
					keyboard: keyboards.cancel,
					resize_keyboard: true
				}
			});
		}
  }

  if(message.text === "🗄 Кабинет") {
  return message.send(`
  👤 Имя: <b>${message.from.first_name.replace(/(\<|\>)/g, '')}</b>

🆔 ID: <code>${message.from.id}</code>

🔑 Статус: ${message.user.verify ? `<b>Спонсор</b>` : `<b>Игрок</b>`}`,
{parse_mode: "HTML",});
 }
 
  if(message.text === "📢 Реклама")
  { return message.send(`🔸 <b>Проект</b> открыт к рекламным предложениям: \n
🔒 <b>Наши контакты:</b> @anonymous_vzlom_error`,
 { parse_mode: "HTML",
 });
  }

	if(message.text === "📃 Правила") {
		return message.send(`<b>🔒 Администрация Бота «Chat Roulette» предоставляет всем пользователям мессенджера возможность пообщаться со случайным собеседником.

🔹 Администрация не несет ответственности за контент распространяемый пользователями. При выявлении нарушений Администрация имеет право забанить на бессрочный срок любого пользователя, нарушающего данные правила. Администрация не может гарантировать, что запрещенная информация будет отсутствовать в сообщениях.

🚫 Запрещено распространять:
— Порнографический контент.
— Оружие, наркотики, психотропные вещества.
— Сообщения призывающие к суициду.
— Сообщения призывающие к массовым беспорядкам.
— Оскорбительные сообщения.
— Экстремистский контент.
— Любые иные вещи, документы или информацию запрещенную к распространению законодательством.</b>`,
  {parse_mode: "HTML",});
	}

	if(message.user.partner) {
	   
	  if(message.text) {
			bot.sendMessage(message.user.partner, message.text,
			{parse_mode: "HTML",});
		}
	    
		if(message.photo) {
			bot.sendPhoto(message.user.partner, message.photo[message.photo.length - 1].file_id, {
			caption: message.caption ? message.caption : ""
			});
		}

		if(message.audio) {
			bot.sendAudio(message.user.partner, message.audio.file_id, {
				caption: message.caption ? message.caption : ""
			});
		}

		if(message.video) {
			bot.sendVideo(message.user.partner, message.video.file_id, {
				caption: message.caption ? message.caption : ""
			});
		}

		if(message.voice) {
			bot.sendVoice(message.user.partner, message.voice.file_id, {
				caption: message.caption ? message.caption : ""
			});
		}

		if(message.video_note) {
			bot.sendVideoNote(message.user.partner, message.video_note.file_id, {
				caption: message.caption ? message.caption : ""
			});
		}

		if(message.sticker) {
			bot.sendSticker(message.user.partner, message.sticker.file_id, {
				caption: message.caption ? message.caption : ""
			});
		}

		if(message.document) {
			return message.send(`📄 Запрещено отправлять документы!`);
		}

		
	}
});

User.prototype.inc = function(field, value = 1) {
	this[field] += value;
	return this.save();
}

User.prototype.dec = function(field, value = 1) {
	this[field] -= value;
	return this.save();
}

User.prototype.set = function(field, value) {
	this[field] = value;
	return this.save();
}
