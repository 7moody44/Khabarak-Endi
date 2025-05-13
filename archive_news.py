import json
import os
from datetime import datetime
import shutil

# Create archive directory if it doesn't exist
ARCHIVE_DIR = 'Old_News'
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

def archive_current_news():
    """Archive current news before updating"""
    try:
        # Check if current news file exists
        if os.path.exists('data/news.json'):
            # Read current news
            with open('data/news.json', 'r', encoding='utf-8') as f:
                current_news = json.load(f)
            
            # Generate timestamp for archive filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_filename = f'news_{timestamp}.json'
            
            # Save to archive directory
            archive_path = os.path.join(ARCHIVE_DIR, archive_filename)
            with open(archive_path, 'w', encoding='utf-8') as f:
                json.dump(current_news, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Successfully archived current news to {archive_filename}")
            return True
    except Exception as e:
        print(f"✗ Error archiving news: {str(e)}")
        return False

def cleanup_old_archives(max_archives=1000):
    """Cleanup old archives if we exceed maximum number"""
    try:
        archives = sorted([f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.json')])
        if len(archives) > max_archives:
            # Remove oldest archives
            archives_to_remove = archives[:-max_archives]
            for archive in archives_to_remove:
                os.remove(os.path.join(ARCHIVE_DIR, archive))
            print(f"✓ Cleaned up {len(archives_to_remove)} old archives")
    except Exception as e:
        print(f"✗ Error cleaning up archives: {str(e)}")

if __name__ == "__main__":
    archive_current_news()
    cleanup_old_archives()