"""
A simple WSGI gateway for Passenger/Nginx
"""
from dds.server import make_app

application = make_app()