__all__ = [
    "NATIVE_REGEX",
    "OperationStatuses",
    "OperationTypes",
    "OperationSources"
]

import enum

NATIVE_REGEX = r"^[+-]?\s*[1-9]\d*([,.]\d{1,2})?$"


class OperationStatuses(enum.IntEnum):
    Created = 0
    Interaction = 1
    Finalized = 2
    Processing = 3
    Uploaded = 4
    Canceled = 5
    Expired = 6
    Error = 7


class OperationTypes(enum.IntEnum):
    Expenses = 0
    Income = 1


class OperationSources(enum.IntEnum):
    Manual = 0
    Monobank = 1
