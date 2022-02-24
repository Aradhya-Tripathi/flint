import click


@click.command("login", help="Login in to fire-watch")
@click.argument("Email")
@click.option("--force-login", is_flag=True, default=False)
def login(email, force_login=False):
    from flint.commands.auth import login

    login(email, force_login)


@click.command("register", help="Register new user")
def register():
    from flint.commands.auth import register

    register()


@click.command("get-data", help="Get logged data")
@click.option("--file", help="/path/to/data/dump")
def get_data(file):
    from flint.commands.user import get_data

    get_data(file)


@click.command("logout", help="Log out current user")
def logout():
    from flint.commands.auth import logout

    logout()


@click.command("reset-password", help="Reset password")
@click.argument("Email")
def reset_password(email: str):
    from flint.commands.auth import reset_password

    reset_password(email)


@click.command("remove-account", help="Delete current user account")
@click.option("--force", is_flag=True, default=False, help="Force remove account")
def remove_account(force=False):
    from flint.commands.user import remove_account

    remove_account(force)


@click.command("whoami", help="Currently logged in user")
@click.option("--verbose", is_flag=True, help="Display all account details")
def whoami(verbose):
    from flint.commands.user import whoami

    whoami(verbose)
