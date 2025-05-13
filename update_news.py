import json
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
import traceback
from archive_news import archive_current_news, cleanup_old_archives

# Your existing headers and sources configuration here
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'ar-YE,ar;q=0.9',
    'Referer': 'https://www.google.com/'
}

def main():
    print("\n" + "="*50)
    print("🚀 NEWS UPDATE AND ARCHIVAL SYSTEM")
    print("="*50 + "\n")
    
    # First archive existing news
    print("Archiving current news...")
    archive_current_news()
    
    # Then proceed with normal news update
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
    
    # Save new results
    with open('data/news.json', 'w', encoding='utf-8') as f:
        json.dump({
            "lastUpdated": datetime.utcnow().isoformat() + "Z",
            "articles": all_articles
        }, f, ensure_ascii=False, indent=2)
    print("\n💾 New articles saved to news.json")
    
    # Cleanup old archives if needed
    cleanup_old_archives()
    
    # Final report
    print("\n" + "="*50)
    print("📊 UPDATE RESULTS")
    print("="*50)
    for name, status in results.items():
        print(f"{name.ljust(25)}: {status}")

if __name__ == "__main__":
    main()