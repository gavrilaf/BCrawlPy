from flask import render_template, jsonify
from app import app

monitor_values = {
	'yandex_search' : 10, 
	'yandex_content' : 20, 
	'lj_content' : 25, 
	'vk_content' : 21,
	'posts_found' : 122,
	'dublicates' : 20,
	'filtered' : 100,
	'persisted' : 102}



def get_monitor_values():
	for k in monitor_values.iterkeys():
		monitor_values[k] += 1

	return monitor_values	


@app.route('/api/v1.0/monitor', methods = ['GET'])
def get_tasks():
    return jsonify( { 'monitor': get_monitor_values() } )

@app.route('/monitor')
def monitor():
    return render_template("monitor.html", monitor = get_monitor_values())