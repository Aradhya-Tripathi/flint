import subprocess
from shlex import split


def execute(cmd, output=False, **kwargs):
    cmd = split(cmd)
    return subprocess.run(cmd, capture_output=output, **kwargs)
