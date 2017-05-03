import os
from server import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = (port == 5000)
    if debug:
        app.config['MONGODB_SETTINGS'] = {'db': 'local_db'}
    app.run(host='0.0.0.0', port=port, debug=debug)
