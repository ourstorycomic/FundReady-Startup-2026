import requests
import os
from dotenv import load_dotenv

load_dotenv('api/.env')
key = os.environ.get('GEMINI_API_KEY')
res = requests.get(f'https://generativelanguage.googleapis.com/v1beta/models?key={key}')
models = res.json().get('models', [])
for m in models:
    print(m['name'])
