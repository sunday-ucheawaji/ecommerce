import requests


endpoint = "http://localhost:8000/products/"
get_response = requests.get(endpoint, params={"abc": 123}, json={"echo": "nothing echo"})

print(get_response.json())
