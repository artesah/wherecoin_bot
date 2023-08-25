__all__ = ["get_now", "get_base_58_string", "make_sign", "module_to_dict"]

import hashlib
import random
from datetime import datetime


def get_now():
    return datetime.now()


def get_base_58_string(length=20) -> str:
    return "".join(
        random.choices(
            "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz", k=length
        )
    )


def make_sign(data, key, items=None, algorithm=hashlib.sha256, delimiter=""):
    if items is None:
        items = list(data)

    items = sorted(items)
    concatenated = delimiter.join(map(str, (data[item] for item in items))) + key

    return algorithm(concatenated.encode("utf-8")).hexdigest()


def module_to_dict(module):
    return {key: getattr(module, key) for key in module.__all__}
