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
dp.middleware.setup(LoggingMiddleware)


class Form(StatesGroup):
    before_start = State()


Form.before_start.set()


@dp.message_handler(state = Form.before_start, commands = ['start'])
async def arch_start(message: types.Message):
    await lg.create_user_table(message.from_user.username)
    await Form.next()


# @dp.message_handler(commands = )