import click
import httpx
from flint import domain, protocal
from flint.hooks import on_failure
from flint.user import User
from flint.utils import _exit
from flint.utils.auth import TokenAuth
from flint.utils.data import dump_json

user = User()

user_client = httpx.Client(
    base_url=protocal + domain,
    headers={"Content-Type": "application/json"},
    http2=True,
    auth=TokenAuth(user.tokens),
    event_hooks={"response": [on_failure]},
)

user_details = "user/details"


def get_data(file):
    response = user_client.get(user_details).json()
    dump_json(response)


def remove_account(ctx, force):
    msg = f"Removed user account for {user}"
    if force:
        response = user_client.delete(user_details)
        user.delete()
        _exit(ctx, msg=msg, fg="yellow", error_code=1, response=response)

    if click.confirm(f"Do you want to remove account for {user}"):
        response = user_client.delete(user_details)
        user.delete()
        _exit(ctx, msg=msg, fg="yellow", error_code=1, response=response)


def whoami(ctx):
    _exit(ctx, msg=f"Currently logged in as {user}", fg="yellow")
