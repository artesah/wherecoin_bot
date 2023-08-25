__all__ = [
    "NATIVE_REGEX",
    "OperationStatuses",
    "OperationTypes"
]

import enum

NATIVE_REGEX = r"^[+-]?\s*[1-9]\d*([,.]\d{1,2})?$"


class OperationStatuses(enum.IntEnum):
    Created = 0
    Interaction = 1
    Finalized = 2
    Processed = 3
    Canceled = 4
    Expired = 5


class OperationTypes(enum.IntEnum):
    Expenses = 0
    Income = 1
