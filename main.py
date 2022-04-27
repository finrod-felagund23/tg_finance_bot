from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
import logic as lg
import logging


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
logging.basicConfig(level = logging.INFO)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands = ['start'])
async def start_process(message: types.Message):
    signal = await lg.create_user_table(message.from_user.username)
    print(signal)
    if signal == 'exists':
        await message.reply('Аккаунт уже существовал!')
    elif signal == 'not exists':
        await message.reply('Аккаунт создан!')


@dp.message_handler(content_types = ['text'])
async def add_expense(message: types.Message):
    status = await lg.add_expense(message)
    await message.reply(status)

if __name__ == '__main__':
    executor.start_polling(dp)
