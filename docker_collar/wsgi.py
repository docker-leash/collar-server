# vim:set ts=4 sw=4 et:
"""
Wsgi
====
"""


from docker_collar.collar_client import create_app

app = create_app(debug=True)
