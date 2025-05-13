import sqlite3

# adjust path if needed:
DB_PATH = 'news_database.db'  # or 'backend/news_database.db'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM articles;")
print("Total articles:", cur.fetchone()[0])

cur.execute("SELECT title, url FROM articles ORDER BY published_date DESC LIMIT 5;")
for title, url in cur.fetchall():
    print("-", title, "|", url)

conn.close()

