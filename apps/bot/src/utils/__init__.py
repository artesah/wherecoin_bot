import logging
from typing import List

from aiogram import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError

from apps.bot.config import BOT_ADMINS


async def send_message_to_list(dp: Dispatcher, chat_ids: List[str], text, **kwargs):
    for chat_id in chat_ids:
        try:
            await dp.bot.send_message(chat_id=chat_id, text=text, **kwargs)
        except TelegramAPIError as ex:
            logging.info(f"Cant send message to {chat_id}. {str(ex)}.")


async def send_message_to_admins(dp: Dispatcher, text: str, **kwargs):
    await send_message_to_list(dp, BOT_ADMINS, text, **kwargs)
