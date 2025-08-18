import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_featured_news(country="us", category="technology", page_size=5):
    """
    Fetches top headlines from NewsAPI.
    Returns a list of dictionaries with title, description, url, image, and source.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("Missing NEWS_API_KEY in .env file.")

    url = (
        "https://newsapi.org/v2/top-headlines"
        f"?country={country}&category={category}&pageSize={page_size}&apiKey={api_key}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

    articles = response.json().get("articles", [])

    # Build cleaned-up news list
    return [
        {
            "title": article.get("title", "No title available"),
            "description": article.get("description", "No description available"),
            "url": article.get("url"),
            "image": article.get("urlToImage"),
            "source": article.get("source", {}).get("name", "Unknown source"),
        }
        for article in articles
    ]
