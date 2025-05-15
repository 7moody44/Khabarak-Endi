import os
import shutil
import json
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
import traceback

# Directory for archived news
OLD_NEWS_DIR = "Old_News"
os.makedirs(OLD_NEWS_DIR, exist_ok=True)

# Save location for current news
NEWS_FILE = "data/news.json"
os.makedirs(os.path.dirname(NEWS_FILE), exist_ok=True)

# HTTP Headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'ar-YE,ar;q=0.9',
    'Referer': 'https://www.google.com/'
}

# Placeholder for your source list
SOURCES = [
    # Example entries (replace with your actual list)
    {
        "name": "Example RSS",
        "type": "rss",
        "url": "https://example.com/rss",
        "category": "General"
    },
    {
        "name": "Example HTML",
        "type": "html",
        "url": "https://example.com/news",
        "category": "General",
        "selectors": {
            "articles": ".article",
            "title": "h2",
            "link": "a"
        }
    }
]

def archive_current_news():
    """Archive the current news.json file before updates."""
    if os.path.exists(NEWS_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = os.path.join(OLD_NEWS_DIR, f"news_{timestamp}.json")
        shutil.copy(NEWS_FILE, archive_file)
        print(f"✅ Archived current news to {archive_file}")
    else:
        print("⚠️ No current news file to archive.")

def fetch_rss(url, source_name, category):
    """Fetch news from RSS feed with detailed logging"""
    try:
        print(f"\n🌐 Attempting RSS: {source_name}")
        print(f"   URL: {url}")
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print("   ❌ Empty RSS feed")
            return []

        articles = []
        for entry in feed.entries[:15]:
            try:
                articles.append({
                    "title": entry.get('title', 'لا يوجد عنوان'),
                    "link": entry.get('link', '#'),
                    "source": source_name,
                    "time": entry.get('published', datetime.now().strftime("%H:%M")),
                    "category": category,
                    "image": entry.get('media_content', [{}])[0].get('url', '') if 'media_content' in entry else ''
                })
            except Exception as e:
                print(f"   ⚠️ RSS item error: {str(e)}")
                continue

        print(f"   ✅ Found {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"   🔥 RSS fetch failed: {str(e)}")
        return []

def fetch_html(url, config):
    """Scrape news from HTML page with detailed debugging"""
    try:
        print(f"\n🌐 Attempting HTML: {config['name']}")
        print(f"   URL: {url}")

        response = requests.get(url, headers=HEADERS, timeout=20)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("   ❌ Bad response from server")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        articles_container = soup.select(config['selectors']['articles'])
        print(f"   Found {len(articles_container)} article containers")

        if not articles_container:
            print("   ❌ No articles found - check CSS selectors")
            print("   First 200 chars of HTML:")
            print(response.text[:200])
            return []

        articles = []
        for item in articles_container[:15]:
            try:
                title = item.select_one(config['selectors']['title']).text.strip()
                link = item.select_one(config['selectors']['link'])['href']

                if not link.startswith('http'):
                    base_url = url.split('/')[0] + '//' + url.split('/')[2]
                    link = base_url + link if link.startswith('/') else base_url + '/' + link

                image = item.select_one('img')['src'] if item.select_one('img') else ''

                articles.append({
                    "title": title,
                    "link": link,
                    "source": config['name'],
                    "time": datetime.now().strftime("%H:%M"),
                    "category": config['category'],
                    "image": image
                })
            except Exception as e:
                print(f"   ⚠️ Article parse error: {str(e)}")
                continue

        print(f"   ✅ Successfully parsed {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"   🔥 HTML fetch failed: {str(e)}")
        print(traceback.format_exc())
        return []

def main():
    print("\n" + "="*50)
    print("🚀 NEWS UPDATE AND ARCHIVAL SYSTEM")
    print("="*50 + "\n")

    # Step 1: Archive old news file
    print("Archiving current news...")
    archive_current_news()

    # Step 2: Fetch from all sources
    all_articles = []
    results = {}

    for source in SOURCES:
        try:
            print(f"\n🔍 Processing: {source['name']} ({source['type'].upper()})")
            if source["type"] == "rss":
                articles = fetch_rss(source["url"], source["name"], source["category"])
            else:
                articles = fetch_html(source["url"], source)

            if articles:
                results[source['name']] = f"✅ SUCCESS ({len(articles)} articles)"
                all_articles.extend(articles)
            else:
                results[source['name']] = "❌ FAILED (0 articles)"
        except Exception as e:
            results[source['name']] = f"🔥 CRASHED: {str(e)}"
            continue

    # Step 3: Final Report
    print("\n" + "="*50)
    print("📊 DIAGNOSTIC RESULTS")
    print("="*50)
    for name, status in results.items():
        print(f"{name.ljust(25)}: {status}")

    # Step 4: Save new results
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    print("\n💾 Results saved to news.json")

if __name__ == "__main__":
    main()
