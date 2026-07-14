from my_api_client import ApiClient, Post

client = ApiClient()
post = client.get_post(1)
print(isinstance(post, Post))