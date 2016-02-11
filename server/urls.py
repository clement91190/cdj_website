from server import app
from flask import render_template


@app.route('/test', methods=['POST', 'GET'])
def test():
    return "Hello World"


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('index.html') 
	
@app.route('/about', methods=['POST', 'GET'])

def about():
	return render_template('about.html')

	@app.route('/vacances', methods=['POST', 'GET'])
def vacances():
	return render_template('vacances.html')
