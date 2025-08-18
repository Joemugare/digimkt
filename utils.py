import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Make sure .env contains NEWS_API_KEY=yourkey

def get_featured_news():
    url = f"https://newsapi.org/v2/everything?q=digital&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok":
        return data.get("articles", [])
    return []
