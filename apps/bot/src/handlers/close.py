from aiogram.types import CallbackQuery

from apps.bot.loader import dp
from apps.bot.src.keyboards.inline import close_callback


@dp.callback_query_handler(close_callback.filter(), state="*")
async def process_close(call: CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.delete()
