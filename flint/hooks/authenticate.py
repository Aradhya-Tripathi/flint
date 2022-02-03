from json import JSONDecodeError
import sys

import click
from httpx import Response


def on_failure(response: Response):
    response.read()
    if response.is_error:
        try:
            message = response.json().get("error")
        except JSONDecodeError:
            message = None
        click.secho(
            f"Request failed with status: {response.status_code}\nmessage: {message}",
            fg="red",
        )
        sys.exit(-1)
