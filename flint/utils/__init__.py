import json
import sys

import click


class _dict(dict):
    def json_data(self):
        return json.dumps(self)


def exit_with_message(msg, fg=None, bg=None, error_code=-1):
    click.secho(msg, fg=fg, bg=bg, err=True)

    sys.exit(error_code)
