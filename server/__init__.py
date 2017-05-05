from flask import Flask
from flask_mongoengine import MongoEngine
from micawber.cache import Cache as OEmbedCache
from micawber import bootstrap_basic


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['ADMIN_PASSWORD'] = 'secret'
app.config['SECRET_KEY'] = '!&b0GDb6m%gFvddrZDj34?_A^pBw9h*'
db = MongoEngine(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'heroku_2ccz1cfc',
    'host': 'mongodb://cdj_blog:unregimentdefromageblanc@ds019478.mlab.com:19478/heroku_2ccz1cfc'
}

# Configure micawber with the default OEmbed providers (YouTube, Flickr, etc).
# We'll use a simple in-memory cache so that multiple requests for the same
# video don't require multiple network requests.appi
oembed_providers = bootstrap_basic(OEmbedCache())


# This is used by micawber, which will attempt to generate rich media
# embedded objects with maxwidth=800.
app.config['SITE_WIDTH'] = 800


import urls
