from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from keyboards.default.main_menu import main_menu


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n"
        f"Я <i>бот</i> для размещения записи\n",
        reply_markup=main_menu,
    )
    if db.select_user(id=message.from_user.id) is None:
        db.add_user(id=message.from_user.id, Name=message.from_user.username)
