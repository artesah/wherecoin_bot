class Service:
    obj_class = None

    def __init__(self, obj):
        if self.obj_class is not None and not isinstance(obj, self.obj_class):
            raise ValueError(
                f"Object must be an instance of " f"{self.obj_class.__name__}"
            )

        self._obj = obj

    @property
    def obj(self):
        return self._obj
