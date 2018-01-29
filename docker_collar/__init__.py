# vim:set ts=4 sw=4 et:

import sys

from flask import Flask

sys.dont_write_bytecode = True


app = Flask(__name__)
app.config.from_object('config')
