import json
import sys
from typing import Any, Dict

import click


def dump_json(data: Dict[Any, Any], indent=4, file=sys.stderr):
    click.secho(json.dumps(data, indent=indent), file=file, fg="green")
