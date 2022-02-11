from json import JSONDecodeError

from httpx import Response

from flint.utils.log import exit_with_message


def on_failure(response: Response):
    response.read()
    if response.is_error:
        try:
            message = response.json().get("error")
        except JSONDecodeError:
            message = None
        finally:
            exit_with_message(msg=message, fg="red", bg="black")
