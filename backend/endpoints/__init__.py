# backend/endpoints/__init__.py
from flask import Flask
from .devices import devices_bp

def register_blueprints(app: Flask):
    app.register_blueprint(devices_bp, url_prefix='/devices')