# vim:set ts=4 sw=4 et:

DEBUG = True
ALLOW_PING = True
ALLOW_READONLY = False

SENTRY_DSN = None

LEASH_URL = "https://docker-leash.kumy.org"
LEASH_CA_CERT = "/certs/ca.pem"
LEASH_CONNECT_TIMEOUT = 5

DOCKER_CA_CERT = "/certs/ca.pem"
DOCKER_CERT_FILE = "/certs/cert.pem"
DOCKER_KEY_FILE = "/certs/key.pem"
DOCKER_URL = "https://127.0.0.1:2376"
DOCKER_CONNECT_TIMEOUT = 5
