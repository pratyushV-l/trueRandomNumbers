import sys
import os

project_home = '/home/pratyushV1'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

os.environ['FLASK_APP'] = 'script.py'

# Importing my Flask app
from script import app as application
