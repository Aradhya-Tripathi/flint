import httpx

from flint import domain, protocal
from flint.commands import flint_commands
from flint.utils.log import exit_with_message


def is_alive():
    try:
        httpx.get("".join([protocal, domain, "/health-check"]))
    except httpx.ConnectError:
        exit_with_message("Server unavailable!", bg="black", fg="red")


def run():
    is_alive()
    flint_commands()
