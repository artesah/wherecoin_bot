from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from apps.bot.loader import dp, content


@dp.message_handler(Command("about"))
async def process_about(message: Message):
    await message.answer(content["messages"]["about"])
