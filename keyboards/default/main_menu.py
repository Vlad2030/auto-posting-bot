from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сделать пост"),
        ],
    ],
    resize_keyboard=True,
)
