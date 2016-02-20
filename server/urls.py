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

@app.route('/inscriptions', methods=['POST', 'GET'])
def inscriptions():
	return render_template('inscriptions.html')
	
@app.route('/projet', methods=['POST', 'GET'])
def projet():
	return render_template('projet.html')
	
@app.route('/statuts', methods=['POST', 'GET'])
def statuts():
	return render_template('statuts.html')
	
@app.route('/camps_6_12', methods=['POST', 'GET'])
def camps_6_12():
	return render_template('camps_6_12.html')
	
@app.route('/camps_13_15', methods=['POST', 'GET'])
def camps_13_15():
	return render_template('camps_13_15.html')
	
@app.route('/camps_16_17', methods=['POST', 'GET'])
def camps_16_17():
	return render_template('camps_16_17.html')
	
@app.route('/jvoupas', methods=['POST', 'GET'])
def jvoupas():
	return render_template('jvoupas.html')