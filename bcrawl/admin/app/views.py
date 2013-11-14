from flask import render_template, jsonify
from app import app
from contextlib import closing
from bcrawl.db import Monitor



def get_cmon_values():
	with closing(Monitor.Repository()) as db:
		return db.status_full()


@app.route('/api/v1.0/cmon', methods = ['GET'])
def get_tasks():
    return jsonify({'monitor' : get_cmon_values()})

@app.route('/status/collecting')
def collecting_status():
    return render_template("collecting_mon.html", monitor=get_cmon_values())

@app.route('/status/queries')
def queries_status():
    return render_template("collecting_status.html")

@app.route('/status/server')
def server_status():
    return render_template("server_mon.html")