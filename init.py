import subprocess
import sys

http = subprocess.Popen([sys.executable, "servers/httpserver.py"])
file = subprocess.Popen([sys.executable, "servers/fileserver.py"])
#chat = subprocess.Popen([sys.executable, "servers/websocketserver.py"])

try:    
    http.wait()
    file.wait()
    #chat.wait()
except KeyboardInterrupt:
    http.terminate()
    file.terminate()
    #chat.terminate()