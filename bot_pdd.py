import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# грузим токен из .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("API_TOKEN не найден в .env")


async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я пар"
    )


async def echo_reverse(message: Message):
    text = message.text or ""
    await message.answer(text[::-1])


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(echo_reverse, F.text)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
