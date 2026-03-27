"""
WSGI entry point for Railway deployment
Properly handles imports from backend directory
"""
import sys
import os

# Add project root to Python path so backend can be imported as a package
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

# Now import the Flask app from backend
from backend.app import app

if __name__ == '__main__':
    app.run()
