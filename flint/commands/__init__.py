import click


@click.group()
def flint_commands():
    """
    Command line tool for Fire-Watch
    """
    import flint


# Authentication
from .commands import login, logout, register, reset_password

flint_commands.add_command(login)
flint_commands.add_command(register)
flint_commands.add_command(logout)
flint_commands.add_command(reset_password)

# User options
from .commands import get_data, remove_account, whoami

flint_commands.add_command(get_data)
flint_commands.add_command(remove_account)
flint_commands.add_command(whoami)
