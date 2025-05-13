#!/usr/bin/env python3
"""
Deployment script for the Yemeni News Website

This script sets up and runs both the backend API server and a simple HTTP server
for the frontend files, making the website accessible locally.
"""

import os
import sys
import subprocess
import time
import signal
import webbrowser
import sqlite3
from pathlib import Path

# Define paths
# Define paths
PROJECT_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_ROOT / 'backend'
FRONTEND_DIR = PROJECT_ROOT / 'frontend'


# Define ports
API_PORT = 5000
FRONTEND_PORT = 8000

# Process holders
api_process = None
frontend_process = None

def setup_database():
    """Set up the SQLite database if it doesn't exist"""
    print("Setting up database...")
    
    # Import the news_aggregator module
    sys.path.append(str(BACKEND_DIR))
    try:
        from news_aggregator import setup_database, initialize_sources
        
        # Run setup functions
        setup_database()
        initialize_sources()
        print("✓ Database setup complete")
        return True
    except Exception as e:
        print(f"✗ Error setting up database: {str(e)}")
        return False

def start_api_server():
    """Start the Flask API server"""
    global api_process
    
    print(f"Starting API server on port {API_PORT}...")
    
    try:
        # Change to backend directory
        os.chdir(BACKEND_DIR)
        
        # Start the API server
        api_process = subprocess.Popen(
            [sys.executable, 'api_server.py'],
            env=dict(os.environ, FLASK_APP='api_server.py', PORT=str(API_PORT))
        )
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Check if the server is running
        if api_process.poll() is None:
            print(f"✓ API server running at http://localhost:{API_PORT}")
            return True
        else:
            print("✗ API server failed to start")
            return False
    
    except Exception as e:
        print(f"✗ Error starting API server: {str(e)}")
        return False

def start_frontend_server():
    """Start a simple HTTP server for the frontend files"""
    global frontend_process
    
    print(f"Starting frontend server on port {FRONTEND_PORT}...")
    
    try:
        # Change to frontend directory
        os.chdir(FRONTEND_DIR)
        
        # Start the HTTP server
        frontend_process = subprocess.Popen(
            [sys.executable, '-m', 'http.server', str(FRONTEND_PORT)]
        )
        
        # Wait a moment for the server to start
        time.sleep(1)
        
        # Check if the server is running
        if frontend_process.poll() is None:
            print(f"✓ Frontend server running at http://localhost:{FRONTEND_PORT}")
            return True
        else:
            print("✗ Frontend server failed to start")
            return False
    
    except Exception as e:
        print(f"✗ Error starting frontend server: {str(e)}")
        return False

def update_frontend_api_url():
    """Update the API URL in the frontend JavaScript file"""
    print("Updating API URL in frontend files...")
    
    js_path = FRONTEND_DIR / 'js' / 'frontend_integration.js'
    
    try:
        # Read the file
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the API URL
        updated_content = content.replace(
            "const API_BASE_URL = 'http://localhost:5000/api';",
            f"const API_BASE_URL = 'http://localhost:{API_PORT}/api';"
        )
        
        # Write the updated content
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✓ API URL updated in frontend files")
        return True
    
    except Exception as e:
        print(f"✗ Error updating API URL: {str(e)}")
        return False

def open_website():
    """Open the website in the default browser"""
    url = f"http://localhost:{FRONTEND_PORT}"
    print(f"Opening website at {url}...")
    
    try:
        webbrowser.open(url)
        print("✓ Website opened in browser")
        return True
    except Exception as e:
        print(f"✗ Error opening website: {str(e)}")
        print(f"Please manually open {url} in your browser")
        return False

def cleanup(signum=None, frame=None):
    """Clean up processes on exit"""
    print("\nShutting down servers...")
    
    if api_process and api_process.poll() is None:
        api_process.terminate()
        api_process.wait()
        print("✓ API server stopped")
    
    if frontend_process and frontend_process.poll() is None:
        frontend_process.terminate()
        frontend_process.wait()
        print("✓ Frontend server stopped")
    
    print("Deployment terminated")
    
    if signum is not None:
        sys.exit(0)

def expose_ports():
    """Expose the ports for external access"""
    print("Exposing ports for external access...")
    
    try:
        # Import the deploy module
        from deploy_expose_port import expose_port
        
        # Expose the API port
        api_result = expose_port(API_PORT)
        print(f"✓ API server exposed at {api_result['url']}")
        
        # Expose the frontend port
        frontend_result = expose_port(FRONTEND_PORT)
        print(f"✓ Frontend server exposed at {frontend_result['url']}")
        
        return {
            'api_url': api_result['url'],
            'frontend_url': frontend_result['url']
        }
    except Exception as e:
        print(f"✗ Error exposing ports: {str(e)}")
        print("External access not available. Website is only accessible locally.")
        return None

def main():
    """Main function to deploy the website"""
    print("\n=== Deploying Yemeni News Website ===\n")
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # Setup steps
    if not setup_database():
        print("Database setup failed. Exiting.")
        return False
    
    if not update_frontend_api_url():
        print("Warning: Failed to update API URL in frontend files.")
    
    if not start_api_server():
        print("API server failed to start. Exiting.")
        cleanup()
        return False
    
    if not start_frontend_server():
        print("Frontend server failed to start. Exiting.")
        cleanup()
        return False
    
    # Open the website
    open_website()
    
    # Expose ports for external access
    exposed_urls = expose_ports()
    
    print("\n=== Deployment Complete ===")
    print("\nLocal Access:")
    print(f"- Frontend: http://localhost:{FRONTEND_PORT}")
    print(f"- API: http://localhost:{API_PORT}/api")
    
    if exposed_urls:
        print("\nExternal Access:")
        print(f"- Frontend: {exposed_urls['frontend_url']}")
        print(f"- API: {exposed_urls['api_url']}/api")
    
    print("\nPress Ctrl+C to stop the servers and exit")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
    
    return True

if __name__ == "__main__":
    main()
