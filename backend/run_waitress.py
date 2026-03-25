import os
import sys
import socket
from waitress import serve
from app import app

# Add backend directory to sys.path to find app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a dummy socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def start_server():
    port = int(os.environ.get('PORT', 5000))
    local_ip = get_local_ip()
    
    universal_url = f"http://{local_ip}:{port}/login"
    
    print("\n" + "="*60)
    print("🚀 SPM SYSTEM: READY FOR ALL DEVICES")
    print("="*60)
    print(f"🔗 USE THIS SINGLE LINK ON BOTH LAPTOP & MOBILE:")
    print(f"   👉 {universal_url}")
    print("-" * 60)
    print(f"💻 (Alternative for Laptop only: http://localhost:{port}/login)")
    print("-" * 60)
    print(f"📁 Serving frontend from: {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')}")
    print("="*60)
    print("\n💡 NOTE: Ensure your phone is on the same WiFi as this PC.")
    print("Press Ctrl+C to stop the server\n")
    
    serve(app, host='0.0.0.0', port=port, threads=4)

if __name__ == "__main__":
    start_server()
