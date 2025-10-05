__all__ = [
    "database",
    "BaseModel",
    "User",
    "OperationCategory",
    "Operation",
    "Chat",
    "MonobankIntegration",
    "set_base_model_mixin",
]

from peewee import (
    DatabaseProxy,
    Model,
    CharField,
    SmallIntegerField,
    DoubleField,
    DateTimeField,
    ForeignKeyField,
    TextField,
    BooleanField,
)
from playhouse.postgres_ext import BinaryJSONField

from libs.constants.constants import OperationStatuses, OperationTypes
from libs.utils import get_now

database = DatabaseProxy()


class class_property(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class BaseModel(Model):
    class Meta:
        database = database

    created_at = DateTimeField(default=get_now)
    updated_at = DateTimeField(null=True)

    @classmethod
    def set_meta(cls, key, value):
        setattr(cls._meta, key, value)

    @classmethod
    def get_by_id(cls, pk):
        try:
            obj: cls = cls.get(cls.id == pk)
            return obj
        except cls.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        self.updated_at = get_now()
        return super().save(*args, **kwargs)

    def set(self, **columns):
        columns_to_update = []

        for name, value in columns.items():
            if name not in self._meta.combined:
                raise ValueError(
                    f"Column {name} does not " f"exist for {self.__class__.__name__}"
                )

            setattr(self, name, value)

            columns_to_update.append(getattr(self.__class__, name))

        self.save(only=columns_to_update)


class User(BaseModel):
    class Meta:
        table_name = "users"

    is_blocked = BooleanField(default=False)
    sheet = CharField(null=True, unique=True)


class Chat(BaseModel):
    class Meta:
        table_name = "chats"

    id = CharField(primary_key=True, index=True)
    user = ForeignKeyField(User, backref="chats_query", unique=True)
    data = BinaryJSONField()


class OperationCategory(BaseModel):
    class Meta:
        table_name = "operation_categories"

    user = ForeignKeyField(User, backref="categories_query")
    name = CharField()
    operation_type = SmallIntegerField()
    is_active = BooleanField(default=True)


class Operation(BaseModel):
    class Meta:
        table_name = "operations"

    user = ForeignKeyField(User, backref="operations_query")
    category = ForeignKeyField(OperationCategory, backref="operations_query", null=True)
    status = SmallIntegerField(default=OperationStatuses.Created)
    type = SmallIntegerField(default=OperationTypes.Unset)
    source = SmallIntegerField()
    amount = DoubleField()
    comment = TextField(null=True)


class MonobankIntegration(BaseModel):
    class Meta:
        table_name = "monobank_integrations"

    user = ForeignKeyField(User, backref="monobank_integrations_query")
    token = CharField()


def set_base_model_mixin(mixin):
    """
    Allows to dynamically set mixin for base model class.
    This func is made to make it possible to add custom global model methods and
    attributes.

    Beware this can brake a lot of things if used carelessly!!!
    """

    BaseModel.__bases__ = (mixin,) + BaseModel.__bases__
