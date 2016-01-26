from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['ADMIN_PASSWORD'] = 'secret'
db = MongoEngine(app)

import urls
