import logging
import asyncio
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")

dp = Dispatcher()
router = Router()

dp.include_router(router)

@dp.message(CommandStart())
async def start(message: Message) -> None:
    keyboard = [
        [KeyboardButton(text='Записаться')],
        [KeyboardButton(text='Мои записи')],
        [KeyboardButton(text='Связаться с администратором')]
    ]
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True, input_field_placeholder='Сделайте выбор...'
    )
    await message.answer("Выберите действие", reply_markup=reply_keyboard)

@router.message(F.text == "Записаться")
async def cmd_signup(message: Message):
    await message.answer("Выберите услугу",reply_markup=signup_inline_keyboard())


@router.message(F.text == "Мои записи")
async def cmd_my_bookings(message: Message):
    await message.answer("У вас пока нет записей")

@router.message(F.text == "Связаться с администратором")
async def cmd_admin(message: Message):
    await message.answer("Свяжитесь с нами по телефону...")

@router.callback_query(F.data.contains("haircut"))
async def man_haircut_result(callback: CallbackQuery):
    dict_names = {
        "man_haircut" : "Мужская стрижка",
        "woman_haircut" : "Женская стрижка",
        "color_haircut" : "Окрашивание"
    }
    await callback.message.edit_text(
        text=f"Вы выбрали услугу: {dict_names[callback.data]}. Теперь выберите мастера."
    )
    await callback.answer()
    
def signup_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Мужская стрижка", callback_data="man_haircut")
    builder.button(text="Женская стрижка", callback_data="woman_haircut")
    builder.button(text="Окрашивание", callback_data="color_haircut")
    builder.adjust(1)
    return builder.as_markup()


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())