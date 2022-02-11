import click
import sys


def exit_with_message(msg, fg=None, bg=None, error_code=-1):
    click.secho(msg, fg=fg, bg=bg, err=True)
    sys.exit(error_code)
