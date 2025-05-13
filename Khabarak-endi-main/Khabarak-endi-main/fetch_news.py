import feedparser
import json
import os
import random
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup

# Define RSS or site homepage sources
SOURCES = {
    "كريتر سكاي": "https://crater-sky.net/",
    "صحافة نت": "https://sahaafa.net/",
    "تعز تودي": "https://taiztoday.net/feed/",
    "المشهد اليمني": "https://www.almashhadnews.com/",
    "اليمن الان": "https://yemennownews.com/",
}

# Function to extract image from an entry
def extract_image(entry):
    if 'media_content' in entry:
        return entry.media_content[0].get('url')
    if 'media_thumbnail' in entry:
        return entry.media_thumbnail[0].get('url')
    if 'content' in entry:
        soup = BeautifulSoup(entry.content[0].value, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
    if 'summary' in entry:
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
    return None

# Function to generate local URL for article
def generate_local_url(title):
    hash_id = hashlib.md5(title.encode('utf-8')).hexdigest()
    return f"show{hash_id}.html"

# Fetch and process news from sources
news_articles = []

for source_name, url in SOURCES.items():
    try:
        feed = feedparser.parse(url)
        entries = feed.entries
        if not entries:
            print(f"⚠️ No entries found for {source_name}")
            continue

        selected_entries = random.sample(entries, min(10, len(entries)))

        for entry in selected_entries:
            title = getattr(entry, "title", "No Title")
            article = {
                "title": title,
                "url": generate_local_url(title),
                "source": source_name,
                "date": getattr(entry, "published", datetime.now().isoformat()),
                "image": extract_image(entry)
            }
            news_articles.append(article)

    except Exception as e:
        print(f"❌ Error fetching from {source_name}: {e}")

# Ensure output directory exists
output_file = "data/news.json"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write to JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({"articles": news_articles}, f, ensure_ascii=False, indent=4)

print(f"✅ Successfully fetched and saved {len(news_articles)} articles to {output_file}.")
