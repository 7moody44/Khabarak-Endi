import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Define both RSS feeds and websites that need direct scraping
SOURCES = [
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "type": "rss"},
    {"name": "Reuters", "url": "https://www.reutersagency.com/feed/?best-regions=Middle-East", "type": "rss"},
    {"name": "Crater Sky", "url": "https://crater-sky.net", "type": "web"},
    {"name": "Sahaafa News", "url": "https://sahaafa.net", "type": "web"}
]

# Function to fetch articles from RSS feeds
def fetch_rss_articles(url, source_name):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        feed = feedparser.parse(response.content)
        articles = []
        for entry in feed.entries[:10]:  # Limit to 10 articles per source
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "source": source_name,
                "date": entry.published if "published" in entry else datetime.utcnow().isoformat() + "Z"
            })
        return articles
    except Exception as e:
        print(f"Error fetching RSS feed {url}: {str(e)}")
        return []

# Function to scrape articles from regular websites
def scrape_web_articles(url, source_name):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = []
            for item in soup.find_all("article")[:10]:  # Adjust for each site's structure
                title_tag = item.find("h2") or item.find("h3")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.find("a")["href"] if title_tag.find("a") else url
                    articles.append({
                        "title": title,
                        "url": link,
                        "source": source_name,
                        "date": datetime.utcnow().isoformat() + "Z"
                    })
            return articles
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return []

# Collect news articles from both RSS and websites
articles = []
for source in SOURCES:
    if source["type"] == "rss":
        articles.extend(fetch_rss_articles(source["url"], source["name"]))
    elif source["type"] == "web":
        articles.extend(scrape_web_articles(source["url"], source["name"]))

# Save articles to JSON
with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump({
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "articles": articles
    }, f, ensure_ascii=False, indent=2)
