# CherryPy + PyWeeRelay = awesome
import cherrypy
from pyweerelay import Relay

class App:
    def __init__(self, relay):
        self.r = relay

    @cherrypy.expose
    def index(self, msg="Hello, world!"):
        self.r.command("python.foo", "print " + msg)
        return '{"status":"success"}'

with Relay("localhost") as r:
    cherrypy.quickstart(App(r))

