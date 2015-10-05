#!/usr/bin/python
import sys
import logging
import os

applicationPath = '/var/www/FlaskApp/FlaskApp'
if applicationPath not in sys.path:
    sys.path.insert(0, applicationPath)

os.chdir(applicationPath)

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/FlaskApp/")

from project import app as application
application.secret_key = '211219898SPKIREW12'
