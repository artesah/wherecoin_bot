import json


def load_content(filename) -> dict:
    with open(filename, "r") as f:
        data = json.loads(f.read())
    return data
