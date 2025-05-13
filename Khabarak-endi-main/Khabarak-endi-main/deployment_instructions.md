# خبرك عندي - Yemeni News Website Deployment Instructions

This document provides detailed instructions for deploying the "خبرك عندي" Yemeni news website on your own server.

## Project Overview

"خبرك عندي" is a news aggregator website that collects and displays news from various Yemeni news sources. The website features:

- RTL (Right-to-Left) support for Arabic content
- Responsive design for desktop, tablet, and mobile devices
- News categorization (politics, economy, sports, culture, etc.)
- Search functionality
- Trending/most read section

## System Requirements

- Python 3.8 or higher
- Web server (Apache, Nginx, etc.)
- SQLite (included with Python)
- Modern web browser

## Required Python Packages

- Flask
- BeautifulSoup4
- Requests

## Project Structure

```
yemeni_news_website/
├── backend/
│   ├── news_aggregator.py     # News scraping and database management
│   ├── api_server.py          # API endpoints for frontend
│   └── frontend_integration.js # JS for frontend-backend integration
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── css/
│   │   └── styles.css         # CSS styles
│   ├── js/
│   │   └── frontend_integration.js # Frontend JS
│   └── images/                # Image assets
├── deploy.py                  # Deployment script
└── deployment_instructions.md # This file
```

## Deployment Steps

### 1. Install Required Packages

```bash
pip install flask beautifulsoup4 requests
```

### 2. Set Up the Database

The database will be automatically set up when you run the deployment script. However, you can manually set it up by running:

```bash
cd /path/to/yemeni_news_website
python -c "from backend.news_aggregator import setup_database, initialize_sources; setup_database(); initialize_sources()"
```

### 3. Start the Backend API Server

```bash
cd /path/to/yemeni_news_website/backend
python api_server.py
```

This will start the Flask API server on port 5000 by default. You can change the port by setting the `PORT` environment variable:

```bash
PORT=8080 python api_server.py
```

### 4. Serve the Frontend Files

You can use any web server to serve the frontend files. For development purposes, you can use Python's built-in HTTP server:

```bash
cd /path/to/yemeni_news_website/frontend
python -m http.server 8000
```

For production, it's recommended to use a proper web server like Apache or Nginx.

#### Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/yemeni_news_website/frontend

    <Directory /path/to/yemeni_news_website/frontend>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPass /api http://localhost:5000/api
    ProxyPassReverse /api http://localhost:5000/api
</VirtualHost>
```

#### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/yemeni_news_website/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Update API URL in Frontend

If you're using a different port or domain for the API server, you'll need to update the API URL in the frontend JavaScript file. Open `/path/to/yemeni_news_website/frontend/js/frontend_integration.js` and modify the `API_BASE_URL` constant:

```javascript
const API_BASE_URL = 'http://your-domain.com/api';
```

### 6. Using the Deployment Script

For convenience, a deployment script is provided that sets up the database, starts the API server, and serves the frontend files:

```bash
cd /path/to/yemeni_news_website
python deploy.py
```

This will:
1. Set up the database if it doesn't exist
2. Start the API server on port 5000
3. Start a simple HTTP server for the frontend on port 8000
4. Open the website in your default browser

## Production Deployment Recommendations

For a production environment, it's recommended to:

1. Use a proper web server (Apache, Nginx) instead of Python's built-in HTTP server
2. Set up a process manager (like Supervisor or systemd) to keep the API server running
3. Consider using a WSGI server (like Gunicorn or uWSGI) for the Flask application
4. Set up SSL/TLS for secure HTTPS connections
5. Configure proper caching for static assets
6. Set up a domain name for your website

## Customization

### Adding New News Sources

To add new news sources, modify the `initialize_sources` function in `backend/news_aggregator.py`:

```python
def initialize_sources():
    """Initialize news sources in the database"""
    sources = [
        # Add your new source here
        {
            'name': 'New Source Name',
            'url': 'https://newsource.com',
            'category': 'general',
            'active': True
        },
        # ...
    ]
    # ...
```

### Modifying the Scraping Logic

The scraping logic for each news source is defined in the `scrape_website` function in `backend/news_aggregator.py`. You may need to modify this function to handle different website structures.

### Customizing the Design

The website design can be customized by modifying the CSS styles in `frontend/css/styles.css`. The color scheme is defined using CSS variables at the top of the file:

```css
:root {
    --primary-color: #CE1126;    /* Red from Yemeni flag */
    --secondary-color: #007A3D;  /* Green from Yemeni flag */
    --neutral-color: #FFFFFF;    /* White from Yemeni flag */
    --background-color: #F5F5F5; /* Light gray */
    --text-color: #333333;       /* Dark gray */
    --accent-color: #000000;     /* Black from Yemeni flag */
    --border-color: #DDDDDD;     /* Light border color */
    --hover-color: #F0F0F0;      /* Hover background color */
}
```

## Troubleshooting

### API Server Won't Start

- Check if port 5000 is already in use. You can change the port by setting the `PORT` environment variable.
- Ensure all required Python packages are installed.
- Check the Flask application logs for error messages.

### Frontend Can't Connect to API

- Ensure the API server is running.
- Check if the API URL in `frontend_integration.js` is correct.
- Check for CORS issues in the browser console.

### News Aggregation Not Working

- Check if the news sources are still active and have the same HTML structure.
- Modify the scraping logic in `news_aggregator.py` if necessary.
- Check the database to ensure sources are properly initialized.

## Support

If you encounter any issues or have questions about the deployment, please contact the developer for assistance.

---

Thank you for using "خبرك عندي" Yemeni News Website!
