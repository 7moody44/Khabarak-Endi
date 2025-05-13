import json
import os
from datetime import datetime
import shutil
import gzip
import sqlite3
from pathlib import Path

# Configure archive settings
ARCHIVE_DIR = 'Old_News'
DB_PATH = os.path.join(ARCHIVE_DIR, 'archives.db')
COMPRESS = True  # Enable compression to save space

def init_db():
    """Initialize SQLite database for archive metadata"""
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS archives
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  timestamp TEXT,
                  article_count INTEGER,
                  size_bytes INTEGER)''')
    conn.commit()
    conn.close()

def archive_current_news():
    """Archive current news with compression"""
    try:
        if not os.path.exists('data/news.json'):
            return False
            
        # Read current news
        with open('data/news.json', 'r', encoding='utf-8') as f:
            current_news = json.load(f)
        
        # Generate archive name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if COMPRESS:
            # Save compressed archive
            archive_filename = f'news_{timestamp}.json.gz'
            archive_path = os.path.join(ARCHIVE_DIR, archive_filename)
            with gzip.open(archive_path, 'wt', encoding='utf-8') as f:
                json.dump(current_news, f, ensure_ascii=False)
        else:
            # Save uncompressed archive
            archive_filename = f'news_{timestamp}.json'
            archive_path = os.path.join(ARCHIVE_DIR, archive_filename)
            with open(archive_path, 'w', encoding='utf-8') as f:
                json.dump(current_news, f, ensure_ascii=False, indent=2)
        
        # Update database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO archives (filename, timestamp, article_count, size_bytes)
                     VALUES (?, ?, ?, ?)''',
                  (archive_filename,
                   timestamp,
                   len(current_news['articles']),
                   os.path.getsize(archive_path)))
        conn.commit()
        conn.close()
        
        print(f"✓ Archived {len(current_news['articles'])} articles to {archive_filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error archiving news: {str(e)}")
        return False

def cleanup_old_archives(max_archives=100, max_size_gb=10):
    """Cleanup old archives based on count and total size"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get total size
        total_size = sum(os.path.getsize(os.path.join(ARCHIVE_DIR, f)) 
                        for f in os.listdir(ARCHIVE_DIR) 
                        if f.endswith(('.json', '.json.gz')))
        total_size_gb = total_size / (1024**3)
        
        # Get archive list ordered by date
        c.execute('SELECT filename FROM archives ORDER BY timestamp DESC')
        archives = c.fetchall()
        
        # Remove oldest archives if we exceed limits
        if len(archives) > max_archives or total_size_gb > max_size_gb:
            archives_to_remove = archives[max_archives:] if len(archives) > max_archives else []
            
            while total_size_gb > max_size_gb and archives:
                archive = archives.pop()
                archives_to_remove.append(archive)
                
                archive_path = os.path.join(ARCHIVE_DIR, archive[0])
                total_size_gb -= os.path.getsize(archive_path) / (1024**3)
            
            # Remove files and database entries
            for archive in archives_to_remove:
                archive_path = os.path.join(ARCHIVE_DIR, archive[0])
                if os.path.exists(archive_path):
                    os.remove(archive_path)
                c.execute('DELETE FROM archives WHERE filename = ?', (archive[0],))
            
            conn.commit()
            print(f"✓ Cleaned up {len(archives_to_remove)} old archives")
            
        conn.close()
        
    except Exception as e:
        print(f"✗ Error cleaning up archives: {str(e)}")

def get_archive_stats():
    """Get statistics about archived news"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*), SUM(article_count), SUM(size_bytes) FROM archives')
        archive_count, total_articles, total_size = c.fetchone()
        
        print("\nArchive Statistics:")
        print(f"Total archives: {archive_count or 0}")
        print(f"Total articles: {total_articles or 0}")
        print(f"Total size: {((total_size or 0) / (1024**2)):.2f} MB")
        
        conn.close()
    except Exception as e:
        print(f"✗ Error getting stats: {str(e)}")

if __name__ == "__main__":
    init_db()
    archive_current_news()
    cleanup_old_archives()
    get_archive_stats()