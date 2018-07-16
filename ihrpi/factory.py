import configparser
import logging
import os

from flask import Flask
from werkzeug.utils import find_modules, import_string


def _get_users():
    config = configparser.ConfigParser()
    config.read(os.getenv('IHRPI_CONF'))
    return {
        config[s]['user']: config[s]['pass']
        for s in config.sections()
    }


def create_app(config=None):
    logging.basicConfig(level=logging.INFO)

    app = Flask('ihrpi')

    app.config.update(dict(
        DEBUG=False,
        BUCKET='some-s3-bucket',  # override me
        PREFIX='packages/simple',  # override me
        USERS=_get_users()
    ))
    app.config.update(config or {})
    app.config.from_envvar('IHRPI_SETTINGS', silent=True)

    register_blueprints(app)
    return app


def register_blueprints(app):
    """Register all blueprint modules."""
    for name in find_modules('ihrpi.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
