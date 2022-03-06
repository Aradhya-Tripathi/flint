import click
import httpx
import websocket
from flint import domain, protocal, websocket_protocal
from flint.hooks import on_close, on_error, on_failure, on_message, on_open
from flint.user import User
from flint.utils import _exit
from flint.utils.auth import TokenAuth, token_from_netrc
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


def get_data(ctx, file):
    response = user_client.get(user_details).json()
    dump_json(response, file=file)


def remove_account(ctx, force):
    msg = f"Removed user account for {user}"
    if force:
        response = user_client.delete(user_details)
        user.delete()
        _exit(ctx=ctx, msg=msg, fg="yellow", error_code=1, response=response)

    if click.confirm(f"Do you want to remove account for {user}"):
        response = user_client.delete(user_details)
        user.delete()
        _exit(ctx=ctx, msg=msg, fg="yellow", error_code=1, response=response)


def whoami(ctx):
    _exit(ctx=ctx, msg=f"Currently logged in as {user}", fg="yellow")


def show_logs(ctx):
    access_token, _ = token_from_netrc(user.tokens)
    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "plain/text",
    }
    ws = websocket.WebSocketApp(
        url=websocket_protocal + domain + "/alerts",
        header=header,
        on_close=on_close,
        on_error=on_error,
        on_message=on_message,
        on_open=on_open,
    )

    ws.run_forever()
