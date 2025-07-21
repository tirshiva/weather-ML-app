import subprocess
import sys
import os
import time

BACKEND_CMD = [sys.executable, '-m', 'uvicorn', 'src.service.api:app', '--reload']
FRONTEND_CMD = [sys.executable, '-m', 'http.server', '8080']

if __name__ == '__main__':
    print('Starting Weather Stats ML Web App...')
    # Start backend
    backend_proc = subprocess.Popen(BACKEND_CMD)
    # Start frontend in web/ directory
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    frontend_proc = subprocess.Popen(FRONTEND_CMD, cwd=web_dir)
    print('\nApp is running!')
    print('Backend:   http://localhost:8000')
    print('Frontend:  http://localhost:8080')
    print('\nPress Ctrl+C to stop both.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nShutting down...')
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print('Stopped.') 