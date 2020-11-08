"""
Created by Epic at 11/7/20
"""
from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge
from waitress import serve

metrics = {}


app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


@app.route("/api/<string:name>", methods=["DELETE", "POST", "PATCH"])
def update_stats(name):
    metric = metrics.get(name, None)
    value = int(request.args.get("value", 1))
    if metric is None:
        metric = Gauge(name, name)
        metrics[name] = metric
    if request.method == "DELETE":
        metric.dec(value)
    elif request.method == "POST":
        metric.inc(value)
    elif request.method == "PATCH":
        metric.set(value)


serve(app, port=5050)
