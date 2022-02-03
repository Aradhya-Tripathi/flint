import click
import httpx
import jwt
from flint import domain, protocal
from flint.hooks.authenticate import on_failure
from flint.utils import _dict
from flint.utils.auth import format_token, load_netrc_file

register_route = "/register"
login_route = "/auth/login"
me = "/user/me"


client = httpx.Client(
    base_url=protocal + domain,
    headers={"Content-Type": "application/json"},
    event_hooks={"response": [on_failure]},
    timeout=10,
    http2=True,
)


def login(email: str, force_login: bool = False):
    netrc = load_netrc_file()

    if not force_login and domain in netrc.hosts:
        creds = netrc.authenticators(domain)
        response = client.get(
            me, headers={"Authorization": f"Bearer {creds[2].split(':')[0]}"}
        )
        click.secho(f"Logged in as {creds[1] or creds[0]}", fg="green")
        return

    password = click.prompt("Enter password", hide_input=True)
    data = _dict(email=email, password=password).json_data
    response = client.post(login_route, data=data)

    credentials = format_token(response.json())
    user_data = jwt.decode(
        credentials.split(":")[0],
        algorithms=["HS256"],
        options={"verify_signature": False},
    )

    netrc.hosts.update(
        {domain: (user_data["email"], user_data["user_name"], credentials)}
    )
    netrc.save()
    click.secho(f"Logged in as {user_data['user_name']}", fg="green")


def register():
    data = _dict(
        user_name=click.prompt("Enter user name"),
        email=click.prompt("Enter email"),
        units=click.prompt("Enter number of units", type=int),
        password=click.prompt(
            "Enter password", confirmation_prompt=True, hide_input=True
        ),
    )
    client.post(register_route, data=data.json_data)
    click.secho(f"Registered {data['user_name']}", fg="green")
