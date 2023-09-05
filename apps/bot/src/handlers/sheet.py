from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from apps.bot.loader import dp, content
from apps.bot.src.filters import UserFilter
from apps.bot.src.keyboards.inline import sheet_url_keyboard


@dp.message_handler(Command("sheet"), UserFilter())
async def process_help(message: Message, current_user):
    await message.answer(
        text=content["messages"]["sheet"],
        reply_markup=await sheet_url_keyboard(current_user.sheet),
    )
