from google.cloud import storage
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def init_storage_client():
    return storage.Client()

def upload_old_news(news_data):
    """Upload old news to Google Cloud Storage"""
    try:
        client = init_storage_client()
        bucket = client.bucket(os.getenv('GOOGLE_CLOUD_BUCKET_NAME'))
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        blob_name = f'old_news_{timestamp}.json'
        
        # Upload the file
        blob = bucket.blob(blob_name)
        blob.upload_from_string(
            json.dumps(news_data, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"✓ Successfully uploaded old news to {blob_name}")
        return True
    except Exception as e:
        print(f"✗ Error uploading to Google Cloud: {str(e)}")
        return False

def get_old_news():
    """Retrieve old news from Google Cloud Storage"""
    try:
        client = init_storage_client()
        bucket = client.bucket(os.getenv('GOOGLE_CLOUD_BUCKET_NAME'))
        
        all_old_news = []
        # List all old news files
        blobs = bucket.list_blobs(prefix='old_news_')
        
        for blob in blobs:
            content = blob.download_as_string()
            news_data = json.loads(content)
            all_old_news.extend(news_data['articles'])
        
        return all_old_news
    except Exception as e:
        print(f"✗ Error retrieving from Google Cloud: {str(e)}")
        return []