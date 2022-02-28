import json
import sys

import click


class _dict(dict):
    @property
    def json_data(self):
        return json.dumps(self)


def exit_with_message(msg, fg=None, bg=None, error_code=-1):
    click.secho(msg, fg=fg, bg=bg, err=True)

    sys.exit(error_code)


def _exit(ctx, msg, **kwargs):
    if ctx.obj["verbose"]:
        if response := kwargs.get("response"):
            msg += f"\nStatus Code: {response.status_code}, Json Response: {response.json()}"

    exit_with_message(
        msg=msg, fg=kwargs.get("fg", "yellow"), error_code=kwargs.get("error_code")
    )
