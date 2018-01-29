# vim:set ts=4 sw=4 et:
"""
The collar for docker leash
===========================
"""

import distutils.util
import json
import logging
import os
import re
import sys

import requests

from docker_collar.enricher import Enricher
from flask import Flask, current_app, jsonify, request
from OpenSSL import crypto as c
from raven.contrib.flask import Sentry

sys.dont_write_bytecode = True

__version__ = "0.0.1.dev0"


def create_app(debug=False):
    """Initialize the application
    """
    app = Flask(__name__)
    app.config.from_object("config")
    app.config.update(
        DEBUG=os.getenv("DEBUG", app.config["DEBUG"]),
        SENTRY_DSN=os.getenv("SENTRY_DSN", app.config["SENTRY_DSN"]),
        ALLOW_PING=os.getenv("ALLOW_PING", app.config["ALLOW_PING"]),
        ALLOW_READONLY=os.getenv("ALLOW_READONLY", app.config["ALLOW_READONLY"]
                                 ),
        LEASH_URL=os.getenv("LEASH_URL", app.config["LEASH_URL"]),
        LEASH_CA_CERT=os.getenv("LEASH_CA_CERT",
                                app.config["LEASH_CA_CERT"]),
        LEASH_CONNECT_TIMEOUT=float(os.getenv("LEASH_CONNECT_TIMEOUT",
                                              app.config["LEASH_CONNECT_TIMEOUT"])),
        DOCKER_URL=os.getenv("DOCKER_URL", app.config["DOCKER_URL"]),
        DOCKER_CA_CERT=os.getenv("DOCKER_CA_CERT", app.config["DOCKER_CA_CERT"]),
        DOCKER_CERT_FILE=os.getenv("DOCKER_CERT_FILE",
                                   app.config["DOCKER_CERT_FILE"]),
        DOCKER_KEY_FILE=os.getenv("DOCKER_KEY_FILE",
                                  app.config["DOCKER_KEY_FILE"]),
        DOCKER_CONNECT_TIMEOUT=float(os.getenv("DOCKER_CONNECT_TIMEOUT",
                                               app.config["DOCKER_CONNECT_TIMEOUT"])),
    )
    if app.config["SENTRY_DSN"]:
        sentry = Sentry(dsn=app.config["SENTRY_DSN"])
        sentry.init_app(app)

    app.logger.handlers[0].formatter._fmt = app.logger.handlers[1].formatter._fmt
    if distutils.util.strtobool(app.config["DEBUG"]):
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.WARNING)

    enricher = Enricher()
    _ping_matcher = re.compile(r'^/_ping$')

    def get_collar_username():
        """Extract the collar username from client certificate
        """
        cert = c.load_certificate(
            c.FILETYPE_PEM,
            file(app.config["DOCKER_CERT_FILE"]).read()
        )
        subject = cert.get_subject().CN
        app.logger.debug("Collar username: %s", subject)
        return subject

    @app.route("/")
    def index():
        """Main entry point. it respond to the `GET` method for the `/` uri.
        """
        return "Docker Collar Plugin"

    @app.route("/Plugin.Activate", methods=["POST"])
    def activate():
        """Entry point for /Plugin.Activate
        """
        return jsonify({"Implements": ["authz"]})

    @app.route("/AuthZPlugin.AuthZReq", methods=["POST"])
    def authz_request():
        """Entry point for /AuthZPlugin.AuthZReq
        """
        # Input payload
        payload = json.loads(request.data)

        if "User" not in payload:
            payload["User"] = None

        if distutils.util.strtobool(app.config["ALLOW_PING"]) and \
                _ping_matcher.match(payload["RequestUri"]):
            app.logger.debug("PING BYPASS FROM CONFIG")
            return jsonify({
                "Allow": True,
                "Msg": "The authorization succeeded."
            })

        if payload["RequestMethod"] == "GET" and \
                distutils.util.strtobool(app.config["ALLOW_READONLY"]):
            app.logger.debug("READONLY BYPASS FROM CONFIG")
            return jsonify({
                "Allow": True,
                "Msg": "The authorization succeeded."
            })

        if payload["User"] == collar_username:
            if payload["RequestMethod"] != "GET":
                app.logger.warn("COLLAR USERNAME DETECTED, BUT HAS READ-ONLY")
                return jsonify({
                    "Allow": False,
                    "Msg": "Collar user has Read-Only permission."
                })

            app.logger.debug("COLLAR USERNAME DETECTED BYPASS LEASH")
            return jsonify({
                "Allow": True,
                "Msg": "The authorization succeeded."
            })

        app.logger.debug("\n\n\n")
        app.logger.info("REQUEST URI: %s", payload["RequestUri"])
        app.logger.info("CONNECTED USERNAME: %s", payload["User"])

        # Enrich request
        payload = enricher.add_host(payload)
        payload = enricher.add_name(payload)
        app.logger.info("REQUEST URI IS NOW: %s", payload["RequestUri"])
        app.logger.debug("REQUEST DATA:\n%s", payload)

        # Forward request to leash-server
        app.logger.debug(
            "CONTACTING LEASH SERVER: %s/AuthZPlugin.AuthZReq" %
            (app.config["LEASH_URL"]))
        response = requests.post(
            "%s/AuthZPlugin.AuthZReq" % (app.config["LEASH_URL"]),
            json=payload,
            headers={
                "Accept": "application/vnd.docker.plugins.v1.2+json",
            },
            verify=app.config["LEASH_CA_CERT"],
            timeout=current_app.config["LEASH_CONNECT_TIMEOUT"],
        )
        app.logger.debug("LEASH SERVER RESPONSE: %s", response.json())

        # Respond
        return jsonify(response.json())

    @app.route("/AuthZPlugin.AuthZRes", methods=["POST"])
    def authz_response():
        """Entry point for /AuthZPlugin.AuthZRes
        """
        return jsonify({
            "Allow": True,
            "Msg": "The authorization succeeded."
        })

    # Call this after route definitions
    collar_username = get_collar_username()
    return app
