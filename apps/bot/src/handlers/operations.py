from aiogram.dispatcher.filters import Regexp
from aiogram.types import Message, CallbackQuery

from apps.bot.loader import dp, content
from apps.bot.src.filters import UserFilter
from apps.bot.src.keyboards.inline import (
    operation_set_category_keyboard,
    operation_set_type_callback,
    operation_set_category_callback,
    operation_cancel_callback,
)
from apps.bot.src.utils.operation import send_operation_message
from libs.constants import NATIVE_REGEX, OperationTypes, OperationStatuses
from libs.constants.constants import OperationSources
from libs.exceptions.exceptions import (
    InvalidNativeError,
    OperationTypeAlreadySetError,
    OperationCategoryAlreadySetError,
    ServiceException,
)
from libs.models import Operation, OperationCategory, User


@dp.message_handler(Regexp(NATIVE_REGEX), UserFilter())
async def process_native(message: Message, current_user: User):
    try:
        operation = Operation.ServiceClass.create_from_native(
            message.text,
            user_id=current_user.id,
            status=OperationStatuses.Interaction,
            source=OperationSources.Manual,
        )
    except InvalidNativeError:
        await message.answer(content["exceptions"]["invalid_native"])
        return

    await send_operation_message(dp.bot, operation)
    await message.delete()


@dp.callback_query_handler(operation_set_type_callback.filter(), UserFilter())
async def process_set_operation_type(
    call: CallbackQuery, callback_data: dict, current_user: User
):
    operation_id = int(callback_data.get("operation_id"))
    operation_type = OperationTypes(int(callback_data.get("operation_type")))

    operation = Operation.get_by_id(operation_id)
    if operation is None:
        await call.answer(content["exceptions"]["operation_not_found"], show_alert=True)
        await call.message.delete()
        return

    try:
        operation.Service.set_type(operation_type)
    except OperationTypeAlreadySetError:
        await call.answer(
            content["exceptions"]["operation_type_already_set"], show_alert=True
        )
        await call.message.delete()
    except ServiceException:
        await call.answer(content["exceptions"]["service_exception"], show_alert=True)
        await call.message.delete()
        return

    await call.answer(cache_time=1)

    await call.message.edit_text(
        content["messages"]["new_operation"].format(
            type=content["constants"]["OperationTypes"][
                OperationTypes(operation.type).name
            ],
            source=content["constants"]["OperationSources"][
                OperationSources(operation.source).name
            ]
            or "",
            amount=operation.amount,
            comment=operation.comment or "",
        )
    )
    await call.message.edit_reply_markup(
        await operation_set_category_keyboard(
            operation.id,
            current_user.Service.get_active_operation_categories(operation.type),
        )
    )


@dp.callback_query_handler(operation_set_category_callback.filter(), UserFilter())
async def process_set_operation_category(
    call: CallbackQuery, callback_data: dict, current_user: User
):
    operation_id = int(callback_data.get("operation_id"))
    category_id = int(callback_data.get("category_id"))

    operation = Operation.get_by_id(operation_id)
    if operation is None:
        await call.answer(content["exceptions"]["operation_not_found"], show_alert=True)
        await call.message.delete()
        return

    category = OperationCategory.get_by_id(category_id)
    if category is None:
        await call.answer(content["exceptions"]["category_not_found"], show_alert=True)
        await call.message.delete()
        return

    try:
        operation.Service.set_category(category_id)
    except OperationCategoryAlreadySetError:
        await call.answer(
            content["exceptions"]["operation_category_already_set"], show_alert=True
        )
        await call.message.delete()
        return
    except ServiceException:
        await call.answer(content["exceptions"]["service_exception"], show_alert=True)
        await call.message.delete()
        return

    try:
        operation.Service.finalize()
    except ServiceException:
        await call.answer(content["exceptions"]["service_exception"], show_alert=True)
        await call.message.delete()
        return

    await call.answer(content["messages"]["operation_finalized"])
    await call.message.delete()


@dp.callback_query_handler(operation_cancel_callback.filter(), UserFilter())
async def process_operation_cancel(
    call: CallbackQuery, callback_data: dict, current_user: User
):
    operation_id = int(callback_data.get("operation_id"))

    operation = Operation.get_by_id(operation_id)
    if operation is None:
        await call.answer(content["exceptions"]["operation_not_found"], show_alert=True)
        await call.message.delete()
        return

    try:
        operation.Service.cancel()
    except ServiceException:
        await call.answer(content["exceptions"]["service_exception"], show_alert=True)
        await call.message.delete()
        return

    await call.answer(content["messages"]["operation_canceled"])
    await call.message.delete()
