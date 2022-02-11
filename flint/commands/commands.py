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
@click.option("--raw", default=False, is_flag=True)
def get_data(file, raw):
    from flint.commands.user import get_data

    get_data(file, raw)
