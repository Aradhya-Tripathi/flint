from json import JSONDecodeError

import click
from httpx import Response
from websocket._exceptions import WebSocketBadStatusException

from flint.utils import _exit


def on_failure(response: Response):
    response.read()
    if response.is_error:
        try:
            message = response.json()["error"]
        except (JSONDecodeError, KeyError):
            message = f"Error Occurred! Status Code: {response.status_code}"
        finally:
            _exit(msg=message, fg="red", error_code=-1)


# Web socket hooks


def on_open(ws, *args):
    click.secho("Connected!", fg="green")


def on_close(ws, *args):
    ws.close()
    _exit(msg="Connection Closed!", fg="red")


def on_error(ws, *args):
    if isinstance(*args, KeyboardInterrupt):
        click.secho("\nClosing Connection!", fg="yellow")
        return
    if isinstance(*args, WebSocketBadStatusException):
        _exit("Authentication Failed please login again!", fg="red")

    click.secho("Error Occured!", fg="yellow")


def on_message(ws, *args):
    print(*args)
