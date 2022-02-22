import os
from datetime import datetime
from netrc import netrc
from typing import Dict

import httpx
import jwt
from flint import domain, protocal
from flint.utils.log import exit_with_message

NETRC_PATH = os.path.join(os.path.expanduser("~"), ".netrc")


class Netrc(netrc):
    def __init__(self, file=None) -> None:
        self.file = file if file else NETRC_PATH
        try:
            super().__init__(self.file)
        except FileNotFoundError:
            open(self.file, "w")
            st = os.stat(self.file)
            os.chmod(self.file, st.st_mode)
        finally:
            super().__init__(self.file)

    def save(self):
        """Hack to save updated netrc file."""
        with open(self.file, "w+") as f:
            data = ""
            for host in self.hosts.keys():
                host_data = self.hosts[host]
                data += f"machine {host}\n\tlogin {host_data[0]}\n"
                if host_data[1]:
                    data += f"\taccount {host_data[1]}\n"
                data += f"\tpassword {host_data[2]}\n"
            f.write(data)


class TokenAuth(httpx.Auth):
    def __init__(self, tokens: str):
        self.access_token, self.refresh_token = tokens.split(":")

    def auth_flow(self, request: httpx.Request):
        request.headers.update({"Authorization": f"Bearer {self.access_token}"})
        initial_request = request
        response = yield request
        if response.status_code == 403:
            request = httpx.Request(
                "get",
                protocal + domain + "/auth/refresh",
                headers={"Authorization": f"Bearer {self.refresh_token}"},
            )
            refresh_response = yield request
            refresh_response.read()

            if refresh_response.is_success:
                self.access_token, self.refresh_token = (
                    refresh_response.json()["access_token"],
                    refresh_response.json()["refresh_token"],
                )
                self.update_tokens()
            else:
                exit_with_message(
                    "Please login again!", fg="red", bg="black", error_code=1
                )
            initial_request.headers.update(
                {"Authorization": f"Bearer {self.access_token}"}
            )
            response = yield initial_request

    def update_tokens(self):
        netrc = Netrc()
        email, user_name, _ = netrc.hosts[domain]
        netrc.hosts.update(
            {
                domain: (
                    email,
                    user_name,
                    ":".join([self.access_token, self.refresh_token]),
                )
            }
        )
        netrc.save()


def format_token(token: Dict[str, str]):
    return ":".join([token.get("access_token"), token.get("refresh_token")])


def token_from_netrc(tokens: str):
    access_token, refresh_token = tokens.split(":")
    return access_token, refresh_token


def is_valid(tokens):
    token, _ = token_from_netrc(tokens)
    payload = jwt.decode(
        token, algorithms=["HS256"], options={"verify_signature": False}
    )
    current_time = datetime.utcnow()
    return datetime.utcfromtimestamp(payload["exp"]) > current_time
