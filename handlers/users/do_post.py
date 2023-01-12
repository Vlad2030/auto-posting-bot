from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import inline_keyboard
from aiogram.types.inline_keyboard import InlineKeyboardButton

from loader import dp, db, bot
from keyboards.inline.moder_post_menu import do_post, do_post_menu
from data.config import ADMINS, CHANNEL_ID


@dp.message_handler(text="Сделать пост")
async def get_post_message(message: types.Message, state: FSMContext):
    await message.answer("Напишите текст для вашей записи")
    await state.set_state("get_message")


@dp.message_handler(state="get_message")
async def get_post_photo(message: types.Message, state: FSMContext):
    await state.update_data({"post": message.text})
    await message.answer("Пришлите мне фотографию для поста")
    await state.set_state("get_photo")


@dp.message_handler(state="get_photo", content_types=ContentType.PHOTO)
async def get_post_photo(message: types.Message, state: FSMContext):
    photo_file = message.photo[-1].file_id
    data = await state.get_data()
    post = data.get("post")

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo_file,
        caption=f"{post}\n" f"\n" f"Отправить?",
        reply_markup=do_post_menu,
    )
    await state.finish()


moderate_post = CallbackData("func", "name", "user_id")


@dp.callback_query_handler(do_post.filter())
async def do_post(call: types.CallbackQuery, callback_data: dict):
    name = callback_data.get("name")
    if name == "yes":
        moderate_post_menu = InlineKeyboardMarkup(
            row_width=3,
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Опубликовать",
                        callback_data=moderate_post.new(
                            name="yes", user_id=call.message.chat.id
                        ),
                    ),
                    InlineKeyboardButton(
                        text="Не публиковать",
                        callback_data=moderate_post.new(
                            name="change", user_id=call.message.chat.id
                        ),
                    ),
                ],
            ],
        )
        for admin in ADMINS:
            message = call.message.caption
            message = message[: message.index("➖")]
            await bot.send_photo(
                chat_id=int(admin),
                caption=message,
                photo=call.message.photo[0]["file_id"],
                reply_markup=moderate_post_menu,
            )
        await call.message.delete()
        await bot.send_message(call.message.chat.id, "Пост отправлен на модерацию")

    else:
        await call.message.delete()
        await bot.send_message(call.message.chat.id, "Пост отменен")


@dp.callback_query_handler(moderate_post.filter())
async def do_post(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get("user_id")
    status = callback_data.get("name")
    if status == "yes":
        await bot.send_photo(
            user_id,
            caption=call.message.caption + "\nStatus: <i>Пост опубликован</i>",
            photo=call.message.photo[0]["file_id"],
        )
        await call.message.edit_caption(
            call.message.caption + "\nStatus:<i> Опубликовано</i>"
        )
        await bot.send_photo(
            CHANNEL_ID,
            caption=call.message.caption,
            photo=call.message.photo[0]["file_id"],
        )
    else:
        await bot.send_photo(
            user_id,
            caption=call.message.caption + "\nStatus: <i>Пост не прошел проверку</i>",
            photo=call.message.photo[0]["file_id"],
        )
        await call.message.edit_caption(
            call.message.caption + "\nStatus:<i> Не опубликовано</i>"
        )
