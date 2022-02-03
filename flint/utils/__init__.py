import json


class _dict(dict):
    @property
    def json_data(self):
        return json.dumps(self)
