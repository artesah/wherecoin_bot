from aiogram.dispatcher.filters import CommandHelp
from aiogram.types import Message

from apps.bot.loader import dp, content


@dp.message_handler(CommandHelp())
async def process_help(message: Message):
    await message.answer(content["messages"]["help"])
