import subprocess


def execute(cmd, output=False, **kwargs):
    if output:
        return subprocess.check_output(cmd, **kwargs)
    return subprocess.call(cmd, **kwargs)
