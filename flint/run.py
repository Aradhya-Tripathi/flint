import httpx

from flint import domain, protocal
from flint.commands import flint_commands
from flint.utils.log import exit_with_message


def run():
    try:
        httpx.get("".join([protocal, domain, "/health-check"]))
    except httpx.ConnectError:
        exit_with_message("Server unavailable!", bg="black", fg="red")

    flint_commands()
