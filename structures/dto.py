from sanic.log import logger


class DTO:
    def __init__(self, data: dict):
        self.data = data
        self.text = data["text"]
        self._additional = data

    def add_additional(self, key, value):
        self._additional[key] = value

    def get(self, key, default=None):
        return self._additional.get(key, default)

    def to_json(self):
        self.data.update(self._additional)
        return self.data
