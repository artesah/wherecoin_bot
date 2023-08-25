from aiogram.dispatcher.filters import (
    CommandStart,
    ChatTypeFilter
)
from aiogram.types import (
    Message,
    ChatType,
)

from apps.bot.config import BLOCK_REGISTRATION
from apps.bot.loader import dp, content
from libs.models import Chat


@dp.message_handler(CommandStart(), ChatTypeFilter(ChatType.PRIVATE))
async def process_start(message: Message):
    chat = Chat.ServiceClass.create_if_not_exists(
        tg_chat_id=message.from_user.id,
        tg_chat_data=message.from_user.as_json(),
        block=BLOCK_REGISTRATION
    )

    if chat.user.is_blocked:
        return

    await message.answer(content["messages"]["start"])
