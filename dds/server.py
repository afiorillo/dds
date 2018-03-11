from flask import Flask, jsonify

from .config import get_config

def make_app(config_file=None, *args, **kwargs):
    # setup app and config
    app = Flask(__name__)
    if config_file is None:
        config = get_config() # uses the defaults
    else:
        config = get_config(config_file)

    # setup routes
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({'status': 'success', 'message': 'the server is alive!'})

    return app