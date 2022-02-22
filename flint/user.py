from flint import domain
from flint.utils.auth import Netrc
from flint.utils.log import exit_with_message


class User:
    def __init__(self):
        self.netrc = Netrc()

    @property
    def tokens(self):
        return self.user()[2]

    def user(self):
        try:
            return self.netrc.hosts[domain]
        except KeyError:
            exit_with_message("Please login or register first!", fg="yellow")
