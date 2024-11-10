from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = ''
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button_formulas = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
button_cal = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kb.add(button_formulas)
kb.add(button_cal)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def get_formula(call):
    await call.message.answer('10 х вес(кг) + 6.25 х рост(см) - 5 х возраст(лет) - 161')
    await call.answer()


class UserClass(StatesGroup):
    age = State()
    height = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserClass.age.set()


@dp.message_handler(state=UserClass.age)
async def set_height(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserClass.height.set()


@dp.message_handler(state=UserClass.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес:')
    await UserClass.weight.set()


@dp.message_handler(state=UserClass.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = (int(data['weight']) * 10) + (int(data['height']) * 6.25) - (5 * int(data['age']))
    await message.answer(f'Ваша норма: {norma} ')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
