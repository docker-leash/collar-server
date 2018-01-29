#!/usr/bin/env python
# vim:set ts=4 sw=4 et:
'''
run
===
'''

from docker_collar.collar_client import app

if __name__ == '__main__':
    app.run(host="0.0.0.0")
