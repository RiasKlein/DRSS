import subprocess
from app import app

subprocess.Popen(["./auth_server/bin/auth_server"])
app.run(host="localhost", port=5000, debug=True)
