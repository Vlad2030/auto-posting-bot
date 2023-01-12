from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

do_post = CallbackData("func", "name")
do_post_menu = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data=do_post.new(name="yes")),
            InlineKeyboardButton(text="Нет", callback_data=do_post.new(name="no")),
        ],
    ],
)
