"""
Created by Epic at 11/7/20
"""
from flask import Flask, request, Request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Gauge, Counter
from waitress import serve
from random import choice
from string import ascii_letters

spawned_pokemons = Gauge("spawned_pokemons", "Pokemons being spawned")
messages = Counter("messages", "Messages sent to the bot")
commands_used_total = Counter("commands_used_total", "Command used (total)")
commands_used_catch = Counter("commands_used_catch", "Command used (catch)")

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})


def add_gauge(gauge: Gauge):
    def inner():
        value = request.args.get("value", 1)
        if request.method == "POST":
            gauge.inc(value)
        else:
            gauge.dec(value)
        return ""

    # Fuck you flask.
    uid = "".join([choice(ascii_letters) for i in range(10)])
    inner.__name__ = uid
    app.route(f"/api/{gauge._name}", methods=["POST", "DELETE"])(inner)


def add_counter(counter: Counter):
    def inner():
        value = request.args.get("value", 1)
        counter.inc(value)
        return ""

    # Fuck you flask.
    uid = "".join([choice(ascii_letters) for i in range(10)])
    inner.__name__ = uid
    app.route(f"/api/{counter._name}", methods=["POST"])(inner)


add_gauge(spawned_pokemons)
add_counter(messages)
add_counter(commands_used_total)
add_counter(commands_used_catch)

serve(app, port=5050)
