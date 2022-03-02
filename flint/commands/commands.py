import click


@click.command("login", help="Login in to fire-watch")
@click.argument("Email")
@click.option("--force-login", is_flag=True, default=False)
@click.option("--password")
@click.pass_context
def login(ctx, email, password, force_login=False):
    from flint.commands.auth import login

    login(ctx, email, force_login, password)


@click.command("register", help="Register new user")
@click.option("--user-name", default=None, help="User name")
@click.option("--email", default=None, help="User email")
@click.option("--units", type=int, default=None, help="Number of units")
@click.option("--password", default=None, help="Password")
@click.pass_context
def register(ctx, user_name, email, units, password):
    from flint.commands.auth import register

    register(ctx, user_name, email, units, password)


@click.command("get-data", help="Get logged data")
@click.option("--file", help="/path/to/data/dump")
@click.pass_context
def get_data(ctx, file):
    from flint.commands.user import get_data

    get_data(ctx, file)


@click.command("logout", help="Log out current user")
@click.pass_context
def logout(ctx):
    from flint.commands.auth import logout

    logout(ctx)


@click.command("reset-password", help="Reset password")
@click.argument("Email")
@click.pass_context
def reset_password(ctx, email: str):
    from flint.commands.auth import reset_password

    reset_password(ctx, email)


@click.command("remove-account", help="Delete current user account")
@click.option("--force", is_flag=True, default=False, help="Force remove account")
@click.pass_context
def remove_account(ctx, force=False):
    from flint.commands.user import remove_account

    remove_account(ctx, force)


@click.command("whoami", help="Currently logged in user")
@click.pass_context
def whoami(ctx):
    from flint.commands.user import whoami

    whoami(ctx)
