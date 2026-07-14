from my_api_client.client import ApiClient
from my_api_client.models import Post

def test_client():
    client = ApiClient()
    result =client.get_post(1)

    assert isinstance(result, Post)
    assert result.id == 1
    assert result.title != ""
    assert result.body != ""
    assert result.userId > 0