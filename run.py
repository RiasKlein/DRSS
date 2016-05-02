import os
import subprocess
from app import app

# only fire up auth_server on main run, not multiple times
if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
	subprocess.Popen(["./auth_server/bin/auth_server"])

app.run(host="localhost", port=5000, debug=True)
