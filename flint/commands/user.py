import click
import httpx
from flint import domain, protocal
from flint.hooks import on_failure
from flint.user import User
from flint.utils.auth import TokenAuth
from flint.utils.data import dump_json
from flint.utils import exit_with_message

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


def remove_account(force):
    msg = f"Removed user account for {user}"
    if force:
        user_client.delete(user_details)
        user.delete()
        exit_with_message(msg=msg, fg="yellow", error_code=1)

    if click.confirm(f"Do you want to remove account for {user}"):
        user_client.delete(user_details)
        user.delete()
        exit_with_message(msg=msg, fg="yellow", error_code=1)


def whoami(verbose):
    if verbose:
        exit_with_message(
            f"""Currenty logged in as {user}\n{user.whoami}""", fg="yellow"
        )

    exit_with_message(f"Currently logged in as {user}", fg="yellow")
