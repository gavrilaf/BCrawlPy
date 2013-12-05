from flask import render_template, jsonify
from app import app
from contextlib import closing

from bcrawl.monitor import MonDB
from bcrawl.reports import ReportContext, QueriesStatus


def get_monitoring_report():
	with closing(MonDB.Repository()) as db:
		return db.status_full()

def get_collecting_status_report():
	with closing(ReportContext.ReportContext(QueriesStatus.Report())) as report:
		return report.get_report()

# REST API
@app.route('/api/v1.0/status/collecting', methods = ['GET'])
def collecting_status_api():
    return jsonify({'monitor' : get_monitoring_report()})

@app.route('/api/v1.0/status/queries', methods = ['GET'])
def queries_status_api():
    return jsonify({'monitor' : get_collecting_status_report()})

# Monitor pages

@app.route('/status/collecting')
def collecting_status():
    return render_template("status_collect.html", monitor = get_monitoring_report())

@app.route('/status/queries')
def queries_status():
    return render_template("status_queries.html", report = get_collecting_status_report())

@app.route('/status/server')
def server_status():
    return render_template("status_server.html")