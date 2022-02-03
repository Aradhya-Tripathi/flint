import os
from netrc import netrc
from typing import Dict


NETRC_PATH = os.path.join(os.path.expanduser("~"), ".netrc")


def load_netrc_file(path=NETRC_PATH):
    try:
        return Netrc(path)
    except FileNotFoundError:
        # Todo: handle later
        return {}


class Netrc(netrc):
    def save(self):
        """Hack to save updated netrc file."""
        with open(NETRC_PATH, "w+") as f:
            data = ""
            for host in self.hosts.keys():
                host_data = self.hosts[host]
                data += f"machine {host}\n\tlogin {host_data[0]}\n"
                if host_data[1]:
                    data += f"\taccount {host_data[1]}\n"
                data += f"\tpassword {host_data[2]}\n"
            f.write(data)


def format_token(token: Dict[str, str]):
    return token.get("access_token") + ":" + token.get("refresh_token")
