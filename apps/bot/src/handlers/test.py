from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from apps.bot.loader import dp, content


@dp.message_handler(Command("test"))
async def process_test(message: Message):
    await message.answer(content["messages"]["test"])
