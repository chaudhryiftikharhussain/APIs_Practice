import requests

response = requests.get("http://127.0.0.1:8000/search-books/Lee")

print(response.status_code)
