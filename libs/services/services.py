__all__ = [
    "init_services",
    "UserService",
    "OperationService",
    "ChatService",
]

import re
from typing import List

from libs.constants import NATIVE_REGEX, OperationTypes, OperationStatuses
from libs.exceptions.exceptions import InvalidNativeError, ServiceException, OperationTypeAlreadySetError, \
    OperationCategoryAlreadySetError
from libs.models import *
from libs.models.models import User, Operation, OperationCategory
from libs.services.base import Service
from libs.services.utils import ServicesMixin


class UserService(Service):
    obj_class = User

    @classmethod
    def create_for_chat(cls, **kwargs) -> User:
        return User.create(**kwargs)

    @classmethod
    def get_by_chat_id(cls, chat_id: int):
        return User.select().join(Chat).where(Chat.id == str(chat_id)).first()

    def get_active_operation_categories(self, operation_type: OperationTypes) -> List[OperationCategory]:
        return list(
            OperationCategory.select().where(
                OperationCategory.user_id == self.obj.id,
                OperationCategory.operation_type == operation_type,
                OperationCategory.is_active
            )
        )


class ChatService(Service):
    obj_class = Chat

    @classmethod
    def create_if_not_exists(cls, tg_chat_id: int, tg_chat_data: dict, block: bool = False) -> Chat:
        chat = Chat.get_by_id(str(tg_chat_id))
        if chat is not None:
            if chat.data != tg_chat_data:
                chat.data = tg_chat_data
                chat.save(only=(Chat.data,))

            return chat

        with database.atomic():
            chat = Chat.create(
                id=str(tg_chat_id),
                data=tg_chat_data,
                user=User.ServiceClass.create_for_chat(is_blocked=block)
            )

        return chat


class OperationService(Service):
    obj_class = Operation

    @classmethod
    def create_from_native(cls, native: str, user: User) -> Operation:
        if not re.match(NATIVE_REGEX, native):
            raise InvalidNativeError

        for replace_args in [(" ", ""), (",", ".")]:
            native = native.replace(*replace_args)

        if native[0] == "+":
            type_ = OperationTypes.Income
        elif native[0] == "-":
            type_ = OperationTypes.Expenses
        else:
            type_ = None

        amount = abs(float(native))

        return Operation.create(
            user_id=user.id,
            amount=amount,
            type=type_
        )

    def set_type(self, type_: OperationTypes) -> None:
        if self.obj.type is not None:
            raise OperationTypeAlreadySetError

        self.obj.set(type=type_)

    def set_category(self, category_id: int) -> None:
        if self.obj.category_id is not None:
            raise OperationCategoryAlreadySetError

        self.obj.set(category_id=category_id)

    @property
    def is_able_to_finalize(self) -> bool:
        if all(
                [
                    self.obj.category_id is not None,
                    self.obj.amount is not None,
                    self.obj.type is not None,
                    self.obj.status < OperationStatuses.Finalized
                ]
        ):
            return True
        return False

    def finalize(self) -> None:
        if not self.is_able_to_finalize:
            raise ServiceException("Operation is not able to finalize")

        self.obj.set(status=OperationStatuses.Finalized)

    def cancel(self) -> None:
        self.obj.set(status=OperationStatuses.Canceled)

    def expire(self) -> None:
        self.obj.set(status=OperationStatuses.Expired)


def init_services():
    User.set_meta("service_class", "UserService")
    Chat.set_meta("service_class", "ChatService")
    Operation.set_meta("service_class", "OperationService")

    set_base_model_mixin(ServicesMixin)
