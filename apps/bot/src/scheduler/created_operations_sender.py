import logging

from aiogram import Bot

from apps.bot.config import CONTENT_FILENAME
from apps.bot.src.content import load_content
from apps.bot.src.keyboards.inline import operation_set_category_keyboard
from libs.constants import OperationStatuses
from libs.models import Operation, User, Chat

_content = load_content(CONTENT_FILENAME)


async def job(bot: Bot):
    created_operations = list(
        Operation.select(
            Operation.id,
            Operation.status,
            Operation.type,
            Operation.source,
            Operation.amount,
            Operation.comment,
            Operation.user_id,
            User.id,
            User.is_blocked,
            Chat.user_id,
            Chat.id,
        )
        .join(User)
        .join(Chat)
        .where(
            Operation.status == OperationStatuses.Created,
            User.is_blocked == False,
            Chat.user_id == User.id,
        )
    )

    for operation in created_operations:
        try:
            await bot.send_message(
                chat_id=operation.user.chat.id,
                text=_content["messages"]["new_operation"].format(
                    type=operation.type,
                    source=operation.source,
                    amount=operation.amount,
                    comment=operation.comment,
                ),
                reply_markup=await operation_set_category_keyboard(
                    operation.id,
                    operation.user.Service.get_active_operation_categories(
                        operation.type
                    ),
                ),
            )
            operation.set(status=OperationStatuses.Interaction)
        except Exception as ex:
            logging.exception(ex)
            operation.set(status=OperationStatuses.Error)
