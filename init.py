import subprocess
import sys

http = subprocess.Popen([sys.executable, "servers/httpserver.py"])
websocket = subprocess.Popen([sys.executable, "servers/websocketserver.py"])

try:
    http.wait()
    websocket.wait()
except KeyboardInterrupt:
    http.terminate()
    websocket.terminate()