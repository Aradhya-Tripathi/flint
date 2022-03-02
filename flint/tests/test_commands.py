import unittest

from flint.tests import execute


class TestCommands(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.accounts = []
        super().__init__(methodName)

    def test_flint(self):
        execute("flint --help")

    def test_user_ops(self):
        response = execute(
            cmd="flint --verbose --no-input register --email test@xyz.com --units 10 --user-name xyz --password xyz_password",
            output=True,
        )
        self.assertIn("Status Code: 201", response.stderr.decode())
        self.accounts.append("test@xyz.com")
        response = execute(
            cmd="flint --verbose --no-input login test@xyz.com --password xyz_password",
            output=True,
        )
        self.assertIn("Status Code: 200", response.stderr.decode())


if __name__ == "__main__":
    unittest.main()
