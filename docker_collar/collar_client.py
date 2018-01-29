# vim:set ts=4 sw=4 et:

import socket

import requests
import json

from flask import jsonify, request

from . import app

__version__ = '0.0.1.dev0'

def setup_app(application):
    """Initialize the application
    """
    application.config["DEBUG"] = True

setup_app(app)

@app.route('/')
def index():
    """Main entry point. it respond to the `GET` method for the `/` uri."""
    return "Docker Collar Plugin"


@app.route("/Plugin.Activate", methods=['POST'])
def activate():
    return jsonify({'Implements': ['authz']})


@app.route("/AuthZPlugin.AuthZReq", methods=['POST'])
def authz_request():
    payload = json.loads(request.data)
    payload["Host"] = socket.getfqdn()

    app.logger.debug("REQUEST DATA:\n%s", payload)
    response = requests.post(
        "https://docker-leash.kumy.org/AuthZPlugin.AuthZReq",
        json=payload,
        headers={
            "Accept": "application/vnd.docker.plugins.v1.2+json",
        },
        verify="/etc/ssl/certs/cacert-root.pem",
    )
    return jsonify(response.json())


@app.route("/AuthZPlugin.AuthZRes", methods=['POST'])
def authz_response():
    return jsonify({
        "Allow": True,
        "Msg": "The authorization succeeded."
    })
