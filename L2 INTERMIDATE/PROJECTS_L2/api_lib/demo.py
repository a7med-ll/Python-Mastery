from my_api_client.client import ApiClient

client = ApiClient()
post = client.get_post(1)
print(post)