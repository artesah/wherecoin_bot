class ServiceException(Exception):
    base_message = None

    def __init__(self, message=None, *args, **kwargs):
        self.message = message or self.base_message

        super().__init__(args, kwargs)

    def __repr__(self):
        return f"ServiceException: {self.message}"


class InvalidNativeError(ServiceException):
    base_message = "InvalidNativeError"


class OperationTypeAlreadySetError(ServiceException):
    base_message = "OperationTypeAlreadySetError"


class OperationCategoryAlreadySetError(ServiceException):
    base_message = "OperationTypeAlreadySetError"
