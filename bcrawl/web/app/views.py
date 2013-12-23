from flask import render_template, jsonify
from app import app
from contextlib import closing

from bcrawl.base import Consts
from bcrawl.monitor import MonDB
from bcrawl.reports import ReportContext, QueriesStatus, PostsTotal


def get_monitoring_report():
	with closing(MonDB.Repository(Consts.MongoDBs.MAIN, Consts.MgColls.MONITOR)) as db:
		return db.status_full()

def get_collecting_status_report():
	with closing(ReportContext.ReportContext(QueriesStatus.Report())) as report:
		report =  report.get_report()
		return report

def get_posts_total_report():
	with closing(ReportContext.ReportContext(PostsTotal.Report())) as report:
		report =  report.get_report()
		return report


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

# Reports pages

@app.route('/reports/total')
def report_total():
    return render_template("report_total.html", report = get_posts_total_report())