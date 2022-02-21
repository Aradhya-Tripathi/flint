import json
import sys
from typing import Any, Dict

import click
from httpx import Response


def dump_json(data: Dict[Any, Any], indent=4, file=sys.stderr):
    if isinstance(data, Response):
        try:
            data = data.json()
        except json.JSONDecodeError:
            data = {"error": f"Coudn't find json data status code: {data.status_code}"}
    click.secho(json.dumps(data, indent=indent), file=file, fg="green")
