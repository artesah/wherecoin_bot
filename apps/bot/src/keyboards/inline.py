from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from apps.bot.config import CONTENT_FILENAME
from apps.bot.src.content import load_content
from libs.constants import OperationTypes
from libs.models import Category

_content = load_content(CONTENT_FILENAME)

close_callback = CallbackData("close")
operation_set_type_callback = CallbackData("operation_set_type", "operation_id", "operation_type")
operation_set_category_callback = CallbackData("operation_set_category", "operation_id", "category_id")
operation_cancel_callback = CallbackData("operation_cancel", "operation_id")

_close_button = [
    InlineKeyboardButton(
        text=_content["keyboards"]["inline"]["close"],
        callback_data=close_callback.new(),
    )
]


async def operation_set_type_keyboard(operation_id: int):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=_content["keyboards"]["inline"]["operation_type_income"],
                callback_data=operation_set_type_callback.new(
                    operation_id=str(operation_id),
                    operation_type=str(OperationTypes.Income.value)
                ),
            ),
            InlineKeyboardButton(
                text=_content["keyboards"]["inline"]["operation_type_expenses"],
                callback_data=operation_set_type_callback.new(
                    operation_id=str(operation_id),
                    operation_type=str(OperationTypes.Expenses.value)
                ),
            ),
        ],
        [
            InlineKeyboardButton(
                text=_content["keyboards"]["inline"]["operation_cancel"],
                callback_data=operation_cancel_callback.new(
                    operation_id=str(operation_id)
                ),
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def operation_set_category_keyboard(operation_id: int, categories: List[Category]):
    inline_keyboard = []

    row = []
    for cat in categories:
        if len(row) >= 2:
            inline_keyboard.append(row)
            row = []

        row.append(
            InlineKeyboardButton(
                text=cat.name,
                callback_data=operation_set_category_callback.new(
                    operation_id=str(operation_id),
                    category_id=str(cat.id)
                ),
            ),
        )
    else:
        inline_keyboard.append(row)

    # for category in categories:
    #     inline_keyboard.append(
    #         [
    #             InlineKeyboardButton(
    #                 text=category.name,
    #                 callback_data=operation_set_category_callback.new(
    #                     operation_id=str(operation_id),
    #                     category_id=str(category.id)
    #                 ),
    #             ),
    #         ]
    #     )

    inline_keyboard.append([
        InlineKeyboardButton(
            text=_content["keyboards"]["inline"]["operation_cancel"],
            callback_data=operation_cancel_callback.new(
                operation_id=str(operation_id)
            ),
        ),
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
