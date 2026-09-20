import subprocess
import sys

http = subprocess.Popen([sys.executable, "servers/httpserver.py"])
file = subprocess.Popen([sys.executable, "servers/fileserver.py"])
ws = subprocess.Popen([sys.executable, "servers/websocketserver.py"])
#game = subprocess.Popen([sys.executable, "servers/fungicideserver.py"])

try:
    http.wait()
    file.wait()
    ws.wait()
    # game.wait()
except KeyboardInterrupt:
    http.terminate()
    file.terminate()
    ws.terminate()
    # game.terminate()