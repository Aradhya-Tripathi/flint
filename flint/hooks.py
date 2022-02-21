from json import JSONDecodeError

from httpx import Response

from flint.utils.log import exit_with_message


def on_failure(response: Response):
    response.read()
    if response.is_error:
        try:
            message = response.json()["error"]
        except (JSONDecodeError, KeyError):
            message = f"Error Occurred! Status Code: {response.status_code}"
        finally:
            exit_with_message(msg=message, fg="red")
