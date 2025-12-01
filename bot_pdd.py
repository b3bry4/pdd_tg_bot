import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


load_dotenv()
BOT_TOKEN = os.getenv("API_TOKEN")


#состояния
class BotMode(StatesGroup):
    learning = State()          # режим прорешивания билетов
    stats = State()             # режим статистики
    marathon = State()          # режим рандомного марафона
    learning_mistakes = State() # режим отработки ошибок

#инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


BILETI_PATHS = [
    "",
]


#клавиатура главного меню
def main_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Решать билеты🧐"),
            types.KeyboardButton(text="Просмотреть статистику📊"),
        ],
        [
            types.KeyboardButton(text="Режим марафона🏃‍♂️"),
            types.KeyboardButton(text="Отработать ошибки🥱"),
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Что будем делать?"
    )


#клавиатура с кнопкой "Назад"
def back_keyboard() -> types.ReplyKeyboardMarkup:
    kb = [[types.KeyboardButton(text="Назад")]]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="«Назад» - выйти в главное меню",
    )


#/start
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Здесь ты можешь проходить билеты ПДД и проверять свои знания. "
        "Выбирай билет и начинай тренировку",
        reply_markup=main_keyboard(),
    )


#удаляет ответ бота
@dp.message(F.text == "Назад")
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    
    msg = await message.answer("Возвращаю в главное меню...")
    await asyncio.sleep(0.1)
    await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)

    await message.answer(
        "Вы в главном меню. Что будем делать?",
        reply_markup=main_keyboard()
    )


#включение режимов бота


#режим решения билетов
@dp.message(F.text == "Решать билеты🧐")
async def enable_learning_mode(message: Message, state: FSMContext):
    await state.set_state(BotMode.learning)
    await message.answer(
        "Выбери вариант билета. Чтобы выйти нажми 'Назад'",
        reply_markup=back_keyboard(),
    )


#режим просмотра статистики
@dp.message(F.text == "Просмотреть статистику📊")
async def enable_stats_mode(message: Message, state: FSMContext):
    await state.set_state(BotMode.stats)
    await message.answer(
        "Ваша статистика:", 
        reply_markup=back_keyboard(),
    )


#режим марафона
@dp.message(F.text == "Режим марафона🏃‍♂️")
async def enable_marathon_mode(message: Message, state: FSMContext):
    await state.set_state(BotMode.stats)
    await message.answer(
        "Режим марафона включен:", 
        reply_markup=back_keyboard(),
        )


#режим отработки ошибок
@dp.message(F.text == "Отработать ошибки🥱")
async def mistakes_mode(message: Message, state: FSMContext):
    await state.set_state(BotMode.stats)
    await message.answer(
        "Режим отработки ошибок включен:", 
        reply_markup=back_keyboard(),
        )




#main
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())