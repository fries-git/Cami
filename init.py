import subprocess
import sys

http = subprocess.Popen([sys.executable, "servers/httpserver.py"])

try:
    http.wait()
except KeyboardInterrupt:
    http.terminate()