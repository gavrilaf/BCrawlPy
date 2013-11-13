#!flask/bin/python
import os, sys

root_dir = os.path.dirname(os.path.abspath('../../'+__file__))
sys.path.append(root_dir)

from app import app

app.run(debug = True)