import json
import os
from typing import Any, Dict

from flint.utils import _exit
from httpx import Response


def dump_json(data: Dict[Any, Any], indent=4, file: str = None):
    if isinstance(data, Response):
        try:
            data = data.json()
        except json.JSONDecodeError:
            data = {"error": f"Coudn't find json data status code: {data.status_code}"}
    if file:
        if os.path.exists(file):
            with open(os.path.join(file), "r+") as f:
                existing_data = json.loads(f.read() or "[]")
                existing_data.append(data)
                f.write(json.dumps(existing_data))
        else:
            with open(os.path.join(file), "w") as f:
                f.write(json.dumps(data, indent=indent))
    else:
        _exit(msg=json.dumps(data, indent=indent), err=True)
