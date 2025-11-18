import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать тест")],
            [KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Привет! Я бот по билетам ПДД.\n"
        "Используй кнопки ниже, чтобы начать.",
        reply_markup=keyboard
    )


@dp.message(F.text == "Начать тест")
async def start_test(message: Message):
    await message.reply("Отлично, выберите вариант!")


@dp.message(F.text == "Помощь")
async def help_me(message: Message):
    await message.reply("Не работает")


async def main():
    dp.message.register(cmd_start, Command("start"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())