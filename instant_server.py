############################
#Very basic python app to start the server.
#Can be used locally for testing.
#To compile the app, use 'export FLASK_APP=instant_server.py'
#The app can then be run using python 'python instant_server.py'
#It requires to have all the python requirements installed ('pip install requirements.txt')
##############################

import os
from server import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = (port == 5000)
    if debug:
        #A local database is used for testing
        app.config['MONGODB_SETTINGS'] = {'db': 'local_db'}
        print('Debug mode is enabled. local_db used')
    app.run(host='0.0.0.0', port=port, debug=debug) #run() should not be used for production. Instead, gunicorn should be used in the procfile
