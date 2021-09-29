import sys

from run import app

sys.path.append("/home/ubuntu/kamodo-deploy/kamodo-dashboard")

app.run_server(host='0.0.0.0')