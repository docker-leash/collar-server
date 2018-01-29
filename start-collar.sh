#!/bin/bash

gunicorn --workers=5 --bind=unix:/run/docker/plugins/collar.sock --reload --access-logfile - --error-logfile - docker_collar.wsgi:app
