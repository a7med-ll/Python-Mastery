import requests
from .models import Post

class ApiClient:

    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url

    def get_post(self, post_id: int) -> Post:

        url = f"{self.base_url}/posts/{post_id}"
        response = requests.get(url)
        response.raise_for_status()
        api_data = response.json()

        return Post(

            userId=api_data["userId"],
            id=api_data["id"],
            title=api_data["title"],
            body=api_data["body"],
        )



