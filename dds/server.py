from flask import Flask, jsonify

from .config import get_config

def make_app(config_file=None, *args, **kwargs):
    # setup app and config
    app = Flask(__name__)
    if config_file is None:
        config = get_config() # uses the defaults
    else:
        config = get_config(config_file)
    config.update(kwargs) # CLI arguments take precedence
    app.config.update(config)

    # setup routes
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({'status': 'success', 'message': 'the server is alive!'})

    return app


def run_server(config_file=None, *args, **kwargs):
    """ Same as make_app, but also runs the app """
    app = make_app(config_file=config_file, *args, **kwargs)
    if config_file is None:
        config = get_config() # uses the defaults
    else:
        config = get_config(config_file)
    config.update(kwargs)  # CLI arguments take precedence
    app.run(host=config['bind_ip'], port=config['bind_port'])