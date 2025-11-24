import os
import asyncio
import logging
import re
import random

import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


load_dotenv()
BOT_TOKEN = os.getenv("API_TOKEN")


BILETI_PATHS = [
    "bileti/",
    # добавить билеты сюда
]



# --------- СОСТОЯНИЯ (FSM) ---------
class BotMode(StatesGroup):
    learning = State()    # режим прорешивания билетов
    stats = State()  # режим статистики
    marathon = State()    # режим рандомных марафона
    learning_mistakes = State() # режим отработки ошибок


    # --------- ИНИЦИАЛИЗАЦИЯ БОТА ---------
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def main_keyboard() -> types.ReplyKeyboardMarkup:
    """Главное меню."""
    kb = [
        [
            types.KeyboardButton(text="Решать билеты🧐"),
            types.KeyboardButton(text="Просмотреть статистику📊"),
        ],
        [
            types.KeyboardButton(text="Режим марафона🏃🏃‍♂️"),
            types.KeyboardButton(text="Отработать ошибки🥱")
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Что будем делать?"
    )




# --------- /start ---------
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # на всякий случай очищаем состояние
    await state.clear()
    await message.answer(
        "Привет! Здесь ты можешь проходить билеты ПДД и проверять свои знания. Выбирай билет и начинай тренировку",
        reply_markup=main_keyboard(),
    )


# --------- КНОПКА НАЗАД (РАБОТАЕТ ИЗ ЛЮБОГО РЕЖИМА) ---------
@dp.message(F.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        ".",
        reply_markup=main_keyboard(),
    )


# --------- MAIN ---------
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())