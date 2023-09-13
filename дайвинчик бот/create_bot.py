import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor



logging.basicConfig(level=logging.INFO)

bot = Bot(token="5664913615:AAExCtaYHihp0iDtHx19_Idzzbm9lwKIBv4")
dp = Dispatcher(bot, storage=MemoryStorage())


