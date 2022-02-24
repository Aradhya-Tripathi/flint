from flint import domain
from flint.utils.auth import Netrc
from flint.utils.log import exit_with_message


class User:
    def __init__(self):
        self.netrc = Netrc()
        try:
            self.user = self.netrc.hosts[domain]
        except KeyError:
            exit_with_message("Please login or register first!", fg="yellow")

    @property
    def tokens(self):
        return self.user[2]

    @property
    def whoami(self):
        return f"User name: {self.user[1]} \t Email: {self.user[0]}"

    def delete(self):
        del self.netrc.hosts[domain]
        self.netrc.save()

    def __repr__(self) -> str:
        return self.user[1]

    def __str__(self) -> str:
        return self.user[1]
