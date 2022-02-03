import typing

import httpx

from flint import domain, protocal
from flint.utils.auth import Netrc


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
