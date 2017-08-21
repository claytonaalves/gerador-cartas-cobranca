import sys
import os
import bottle
sys.path = ['/var/www/gerador-cartas-cobranca/'] + sys.path

os.chdir(os.path.dirname(__file__))

os.environ['DB_HOST'] = "0.0.0.0"
os.environ['DB_USER'] = "user"
os.environ['DB_PASSWORD'] = "password"
os.environ['DB_NAME'] = "vigo"

import app
application = bottle.default_app()



