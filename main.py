"""
Created by Epic at 11/7/20
"""
from flask import Flask, request, Request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge
from waitress import serve

currently_spawned_pokemons = Gauge("currently_alive_pokemons", "Pokemons alive")

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


def process_gauge(gauge):
    gauge.inc() if request.method == "POST" else gauge.dec(1)
    return ""


@app.route("/api/currently_alive_pokemons", methods=["POST", "DELETE"])
def change_currently_alive_pokemon():
    return process_gauge(currently_spawned_pokemons)


serve(app, port=5050)
