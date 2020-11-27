"""
Created by Epic at 11/7/20
"""
from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge, Counter, Histogram
from waitress import serve

metrics = {}
analytic_types = {
    "gauge": Gauge,
    "counter": Counter,
    "histogram": Histogram
}

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


@app.route("/api/<string:name>/<string:analytic_type>", methods=["DELETE", "POST", "PATCH"])
def update_stats(name, analytic_type):
    metric = metrics.get(name, None)
    value = int(request.args.get("value", 1))
    if metric is None:
        metric_type = analytic_types.get(analytic_type)
        if metric_type is None:
            return None, 404
        metric = metric_type(name, name)
        metrics[name] = metric
    if request.method == "DELETE":
        metric.dec(value)
    elif request.method == "POST":
        if isinstance(metric, Histogram):
            metric.observe(value)
            return ""
        metric.inc(value)
    elif request.method == "PATCH":
        metric.set(value)
    return ""


serve(app, port=5050)
