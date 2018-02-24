# vim:set ts=4 sw=4 et:
"""
Enricher
========
"""

import re
import socket

import requests

from flask import current_app


class Enricher(object):
    """Add values not present in the original request.

    :class:`Enricher` is responsible for adding the hostname docker is correctly
     running on to the original request . It also replace image or containers
    ids by the textual name.
    """

    def __init__(self):
        """Initialize the :class:`Enricher`
        """
        matchers = []

        matchers.append({
            "pattern": re.compile(r"/.*/containers/(.+)/.+"),
            "func": self._find_container_name
        })

        matchers.append({
            "pattern": re.compile(r"/.*/images/(.+)/.+"),
            "func": self._find_image_name
        })

        self.matchers = matchers

    def add_host(self, payload):
        """Add the current hostname to the request as 'Host' field.

        :param dict payload: The payload to enrich.
        :return: The payload enriched with 'Host'.
        :rtype: dict
        """
        payload["Host"] = socket.getfqdn()
        return payload

    def add_name(self, payload):
        """Replace id found in url.

        :param dict payload: The payload to enrich.
        :return: The payload with replaced Uri parts.
        :rtype: dict
        """
        uri = payload["RequestUri"]
        for matcher in self.matchers:
            identifier = matcher["pattern"].search(uri)
            if identifier:
                current_app.logger.debug("FOUND AN ID IN URI: %s" % identifier.group(1))
                # Contact dockerd for inspection
                name = matcher["func"](identifier.group(1))
                if name:
                    current_app.logger.debug("FOUND NAME: %s" % name)
                    payload["RequestUri"] = uri.replace(identifier.group(1), name)
                return payload
        return payload

    def _request(self, url):
        """Request the docker daemon.

        :param str url: The url to inspect identifier.
        :return: The inspection result.
        :rtype: dict
        """
        current_app.logger.debug("_request")
        response = requests.get(
            "%s/%s" % (current_app.config["DOCKER_URL"], url),
            verify=current_app.config["DOCKER_CA_CERT"],
            cert=(
                current_app.config["DOCKER_CERT_FILE"],
                current_app.config["DOCKER_KEY_FILE"]
            ),
            timeout=current_app.config["DOCKER_CONNECT_TIMEOUT"],
        )
        return response.json()
        # current_app.logger.debug("JSON RESPONSE: %s" % j_resp)

    def _find_container_name(self, identifier):
        """Find container name.

        :param str identifier: The id to lookup.
        :return: The container name or empty str.
        :rtype: str
        """
        current_app.logger.debug("_add_container_name")
        j_resp = self._request("containers/%s/json" % (identifier))
        if "Name" in j_resp:
            name = j_resp["Name"]
            if name and name[0] == "/":
                name = name.replace("/", "", 1)
            return name
        return ""

    def _find_image_name(self, identifier):
        current_app.logger.debug("_add_image_name")
        j_resp = self._request("images/%s/json" % (identifier))
        # current_app.logger.debug("JSON RESPONSE: %s" % j_resp)
        if "RepoTags" in j_resp:
            return j_resp["RepoTags"][0]
        return ""
