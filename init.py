import subprocess
import sys

http = subprocess.Popen([sys.executable, "servers/httpserver.py"])
img = subprocess.Popen([sys.executable, "servers/imageserver.py"])
ws = subprocess.Popen([sys.executable, "servers/websocketserver.py"])

try:
    http.wait()
    img.wait()
    ws.wait()
except KeyboardInterrupt:
    http.terminate()
    img.terminate()
    ws.terminate()