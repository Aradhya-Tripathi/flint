import click
import httpx
import jwt
from flint import domain, protocal
from flint.hooks import on_failure
from flint.utils import _dict, _exit
from flint.utils.auth import Netrc, format_token, is_valid, token_from_netrc

# Ambiguous route :)
register_route = "/register"

# Auth routes
login_route = "/auth/login"
logout_route = "/auth/logout"
reset_password_route = "/auth/reset-password"
me = "/user/me"


client = httpx.Client(
    base_url=protocal + domain,
    headers={"Content-Type": "application/json"},
    event_hooks={"response": [on_failure]},
    timeout=10.0,
    http2=True,
)
netrc = Netrc()


def login(ctx, email: str, force_login: bool = False, password: str = None):
    if not force_login and domain in netrc.hosts and netrc.hosts[domain][1] == email:
        creds = netrc.authenticators(domain)
        if is_valid(creds[2]):
            _exit(
                ctx,
                msg=f"Logged in as {creds[1] or creds[0]}",
                fg="green",
                error_code=0,
            )

        del netrc.hosts[domain]
        netrc.save()
    password = (
        (click.prompt("Enter password", hide_input=True) if not password else password)
        if not ctx.obj["no_input"]
        else password
    )
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
    msg = f"Logged in as {user_data['user_name']}"
    _exit(
        ctx,
        msg,
        response=response,
        fg="green",
    )


def register(ctx, user_name, email, units, password):
    if ctx.obj["no_input"]:
        data = _dict(
            user_name=user_name,
            email=email,
            units=units,
            password=password,
        )
    else:
        data = _dict(
            user_name=click.prompt("Enter user name"),
            email=click.prompt("Enter email"),
            units=click.prompt("Enter number of units", type=int),
            password=click.prompt(
                "Enter password", confirmation_prompt=True, hide_input=True
            ),
        )
    response = client.post(register_route, data=data.json_data)
    msg = f"Registered {data['user_name']}"
    _exit(ctx, msg, fg="green", response=response)


def logout(ctx):
    if creds := netrc.authenticators(domain):
        access_token, refresh_token = token_from_netrc(creds[2])
        data = _dict(access_token=access_token, refresh_token=refresh_token).json_data
        response = client.post(logout_route, data=data)
        del netrc.hosts[domain]
        netrc.save()
        msg = f"Logged out {creds[1]}"
        _exit(ctx, msg, response=response, fg="green", error_code=0)
    else:
        _exit(
            ctx,
            msg=f"No user logged in!",
            fg="yellow",
            error_code=-1,
        )


def reset_password(ctx, email: str):
    old_passwd = click.prompt("Old Password", hide_input=True)
    new_passwd = click.prompt("New Passowrd", confirmation_prompt=True, hide_input=True)

    data = _dict(email_id=email, old_passwd=old_passwd, new_passwd=new_passwd).json_data
    client.post(reset_password_route, data=data)
    login(email=email, force_login=True, password=new_passwd)
