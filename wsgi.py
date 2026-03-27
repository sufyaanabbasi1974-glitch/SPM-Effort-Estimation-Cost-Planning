"""
WSGI entry point for Railway deployment
Properly handles imports from backend directory
"""
import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Now import and run the app
from app import app

if __name__ == '__main__':
    app.run()
