import requests
import json

url = "http://localhost:8001/api/match-profile"
data = {
    "description": "Startup nông nghiệp công nghệ cao, mới thành lập, đang phát triển MVP",
    "top_n": 1
}
response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
