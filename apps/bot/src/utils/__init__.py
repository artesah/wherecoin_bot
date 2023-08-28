import logging
from typing import List

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError

from apps.bot.config import BOT_ADMINS, CONTENT_FILENAME
from apps.bot.src.content import load_content
from apps.bot.src.keyboards.inline import operation_set_type_keyboard, operation_set_category_keyboard
from libs.models import Operation

_content = load_content(CONTENT_FILENAME)


async def send_message_to_list(dp: Dispatcher, chat_ids: List[str], text, **kwargs):
    for chat_id in chat_ids:
        try:
            await dp.bot.send_message(chat_id=chat_id, text=text, **kwargs)
        except TelegramAPIError as ex:
            logging.info(f"Cant send message to {chat_id}. {str(ex)}.")


async def send_message_to_admins(dp: Dispatcher, text: str, **kwargs):
    await send_message_to_list(dp, BOT_ADMINS, text, **kwargs)
