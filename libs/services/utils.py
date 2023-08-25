class class_property(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class ServicesMixin:
    @class_property
    def ServiceClass(cls):
        if cls._meta.service_class is None:
            raise ValueError(
                f"Service class is not configured for " f"{cls.__name__} model"
            )

        # workaround circular imports (i think there is a better solution)
        import libs.services as services

        return getattr(services, cls._meta.service_class)

    @property
    def Service(self):
        return self.ServiceClass(self)
