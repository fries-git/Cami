import subprocess
import sys

server = subprocess.Popen([sys.executable, "servers/httpandimageserver.py"])

try:
    server.wait()
except KeyboardInterrupt:
    server.terminate()