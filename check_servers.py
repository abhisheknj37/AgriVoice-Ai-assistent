#!/usr/bin/env python3
import socket
import sys

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

print("Checking ports...")
print(f"Port 3000 (Frontend): {'✅ Running' if check_port(3000) else '❌ Not running'}")
print(f"Port 8000 (Backend): {'✅ Running' if check_port(8000) else '❌ Not running'}")

# If servers not running, provide instructions
if not check_port(3000):
    print("\n⚠️  Frontend not running! Start with:")
    print("  cd d:\\agrivoice\\agrivoice-ui")
    print("  npm start")

if not check_port(8000):
    print("\n⚠️  Backend not running! Start with:")
    print("  cd d:\\agrivoice\\backend")
    print("  python manage.py runserver")