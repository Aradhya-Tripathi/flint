import sys

import click

from flint import domain
from flint.utils.auth import Netrc


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
            click.secho("Please login first using flint login", fg="red")
            sys.exit(-1)
