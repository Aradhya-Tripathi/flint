import click

from .commands import login, register


@click.group()
def flint_commands():
    """
    Command line tool for Fire-Watch
    """
    import flint


flint_commands.add_command(login)
flint_commands.add_command(register)
