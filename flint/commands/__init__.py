import click


@click.group()
def flint_commands():
    """
    Command line tool for Fire-Watch
    """
    import flint


# Authentication
from .commands import login, register

flint_commands.add_command(login)
flint_commands.add_command(register)

# User options
from .commands import get_data

flint_commands.add_command(get_data)
