#!/usr/bin/env python3
import subprocess
import os
import time
import sys

def start_servers():
    print("🚀 Starting AgriVoice Application")
    print("=" * 50)
    
    backend_cmd = [
        sys.executable, "manage.py", "runserver"
    ]
    
    frontend_cmd = "npm install && npm start"
    
    # Start backend
    print("\n[1/2] Starting Backend on http://localhost:8000...")
    print("================")
    backend_process = subprocess.Popen(
        backend_cmd,
        cwd=r"d:\agrivoice\backend",
        shell=True
    )
    
    time.sleep(3)
    
    # Start frontend
    print("\n[2/2] Starting Frontend on http://localhost:3000...")
    print("================")
    frontend_process = subprocess.Popen(
        frontend_cmd,
        cwd=r"d:\agrivoice\agrivoice-ui",
        shell=True
    )
    
    print("\n" + "=" * 50)
    print("✅ Both servers are starting...")
    print("🌐 Frontend: http://localhost:3000")
    print("🔌 Backend:  http://localhost:8000")
    print("\n⏳ Waiting for servers to fully start...")
    print("Press Ctrl+C to stop both servers")
    
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    start_servers()