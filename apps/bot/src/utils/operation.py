from aiogram import Bot

from apps.bot.config import CONTENT_FILENAME
from apps.bot.src.content import load_content
from apps.bot.src.keyboards.inline import operation_set_category_keyboard, operation_set_type_keyboard
from libs.constants import OperationSources, OperationTypes
from libs.models import Operation, Chat

_content = load_content(CONTENT_FILENAME)


async def send_operation_message(bot: Bot, operation: Operation):
    text = _content["messages"]["new_operation"].format(
        type=_content["constants"]["OperationTypes"][OperationTypes(operation.type).name],
        source=_content["constants"]["OperationSources"][OperationSources(operation.source).name] or "",
        amount=operation.amount,
        comment=operation.comment or "",
    )

    if operation.type is None:
        reply_markup = await operation_set_type_keyboard(operation.id)
    else:
        reply_markup = await operation_set_category_keyboard(
            operation.id,
            operation.user.Service.get_active_operation_categories(operation.type))

    chat = Chat.select(Chat.id).where(Chat.user_id == operation.user_id).first()
    await bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=reply_markup
    )
