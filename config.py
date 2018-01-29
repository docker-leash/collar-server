# vim:set ts=4 sw=4 et:

DEBUG = True
ALLOW_PING = True
ALLOW_READONLY = False

LEASH_URL = "https://docker-leash.kumy.org"
LEASH_CA_CERT = "/home/kumy/GIT/docker-collar/certs/ca.pem"
LEASH_CONNECT_TIMEOUT = 5

DOCKER_CA_CERT = "/home/kumy/GIT/docker-collar/certs/cacert-root.pem"
DOCKER_CERT_FILE = "/home/kumy/GIT/docker-collar/certs/kumy-nuc-collar.crt"
DOCKER_KEY_FILE = "/home/kumy/GIT/docker-collar/certs/kumy-nuc-collar.key"
DOCKER_URL = "https://kumy-nuc.kumy.org:2376"
DOCKER_CONNECT_TIMEOUT = 5
