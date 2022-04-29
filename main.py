"""
TODO:
Фнукционал изменения категорий
1. Удаление
2. Перезапись
3. Создание
И пока что этого хватит(главное покрыть тестами и коментариями!
"""

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from config import TOKEN
import logic as lg
import logging

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
logging.basicConfig(level = logging.INFO)
dp.middleware.setup(LoggingMiddleware())


class Settings(StatesGroup):
    settings_menu = State()
    category_create = State()
    category_change = State()
    category_delete = State()


@dp.message_handler(commands = ['cancel'], state = '*')
@dp.message_handler(Text(equals = 'отмена', ignore_case = True))
async def cancel_hadler(message: types.Message, state: FSMContext) -> None:
    # TODO very strange handler... FIX
    await state.reset_state()
    await message.reply('Canceled')


@dp.message_handler(commands = ['start'])
async def start_process(message: types.Message) -> None:
    signal = await lg.create_user_table(message.from_user.username)
    print(signal)
    if signal == 'exists':
        await message.reply('Аккаунт уже существовал!')
    elif signal == 'not exists':
        await message.reply('Аккаунт создан!')


@dp.message_handler(commands = ['settings'])
async def settings_handler(message: types.Message) -> None:
    await Settings.settings_menu.set()
    markup = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add('change', 'delete')
    markup.add('create new')

    await message.reply('Выберите вариант', reply_markup = markup, reply = False)


@dp.message_handler(state = Settings.settings_menu, content_types = ['text'])
async def settings(message: types.Message) -> None:
    if message.text == 'delete':
        await Settings.category_delete.set()
    elif message.text == 'change':
        await Settings.category_change.set()
    elif message.text == 'create new':
        await Settings.category_create.set()
    await message.reply('Введите название категории')


@dp.message_handler(state = Settings.category_delete)
async def delete_category(message: types.Message) -> None:
    if len(message.text.split()) > 1:
        await message.reply('Неверное название категории!')
        return
    ans = await lg.delete_category(message)
    await message.reply(ans, reply = False, reply_markup = types.ReplyKeyboardRemove())


@dp.message_handler(state = Settings.category_change)
async def change_category(message: types.Message) -> None:
    if len(message.text.split()) > 1:
        await message.reply('Неверное название категории!')
        return
    ans = await lg.change_category(message)
    await message.reply(ans, reply = False, reply_markup = types.ReplyKeyboardRemove())


@dp.message_handler(state = Settings.category_create)
async def create_new_category(message: types.Message) -> None:
    if len(message.text.split()) > 1:
        await message.reply('Неверное название категории!')
        return
    ans = await lg.create_new_category(message)
    await message.reply(ans, reply = False, reply_markup = types.ReplyKeyboardRemove())


@dp.message_handler(content_types = ['text'])
async def add_expense(message: types.Message) -> None:
    status = await lg.add_expense(message)
    await message.reply(status)


if __name__ == '__main__':
    executor.start_polling(dp)
