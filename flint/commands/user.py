import httpx
from flint import domain, protocal
from flint.hooks import on_failure
from flint.user import User
from flint.utils.auth import TokenAuth
from flint.utils.data import dump_json

user = User()

user_client = httpx.Client(
    base_url=protocal + domain,
    headers={"Content-Type": "application/json"},
    http2=True,
    auth=TokenAuth(user.tokens),
    event_hooks={"response": [on_failure]},
)

user_details = "user/details"


def get_data(file):
    response = user_client.get(user_details).json()
    dump_json(response)
