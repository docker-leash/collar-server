#!/bin/bash

{
    date
    pwd
    ps axu

    ls -l /run
    ls -l /run/docker
    ls -l /run/docker/plugins

    gunicorn --workers=5 --bind=unix:/run/docker/plugins/collar.sock --reload --access-logfile - --error-logfile - docker_collar.wsgi:app

} 2>&1 | tee -a /tmp/test
