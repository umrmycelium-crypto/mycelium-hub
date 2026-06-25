import requests

print("Mycelium CLI online")

r = requests.get("http://localhost:8000/health")
print(r.json())
