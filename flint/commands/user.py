import httpx
from flint import domain, protocal
from flint.auth import TokenAuth
from flint.user import User


user = User()

user_client = httpx.Client(
    base_url=protocal + domain,
    headers={"Content-Type": "application/json"},
    http2=True,
    auth=TokenAuth(user.tokens),
)

user_details = "user/details"


def get_data():
    response = user_client.get(user_details)
