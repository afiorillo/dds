from sys import stderr
from json import dumps
import httplib
from collections import OrderedDict as od

from flask import Flask, jsonify, redirect, url_for, send_file

from .config import get_config
from .util import Path
import renderers

def make_app(config_file=None, *args, **kwargs):
    # setup app and config
    app = Flask(__name__)
    if config_file is None:
        config = get_config() # uses the defaults
    else:
        config = get_config(config_file)
    config.update(kwargs) # CLI arguments take precedence
    app.config.update(config)
    app.static_folder = config['static_dir']

    # handles arbitrarily deep paths
    def serve_file_wrapper(relpath): return serve_file(relpath, config)
    app.add_url_rule('/<path:relpath>', 'serve_file', serve_file_wrapper)

    # handle the no-path case
    @app.route('/', methods=['GET'])
    def nopath():
        return redirect(url_for('serve_file', relpath='index.html'))

    return app


def run_server(config_file=None, *args, **kwargs):
    """ Same as make_app, but also runs the app """
    app = make_app(config_file=config_file, *args, **kwargs)
    if config_file is None:
        config = get_config() # uses the defaults
    else:
        config = get_config(config_file)
    config.update(kwargs)  # CLI arguments take precedence

    cstr = dumps(config, sort_keys=True, indent=2)
    stderr.write(' * active config: \n')
    for l in cstr.split('\n'):
        stderr.write(' * ' + l.strip() + '\n')
    stderr.write(' * \n')
    stderr.flush()

    app.run(host=config['bind_ip'], port=config['bind_port'])


def serve_file(relpath, config):
    # if there is no extension, they must be giving a directory. serve the inner index.html.
    # TODO: better extension detection
    if '.' not in relpath:
        relpath = relpath.rstrip('/') + '/index.html'
        return redirect(relpath)

    # convert relpath into a full directory (under public_dir) and a file
    fp = Path(config['public_dir']).joinpath(relpath)
    dir = fp.parent
    file = fp.name

    if not dir.exists():
        resp = jsonify({
            'status': 'client error',
            'message': 'directory "%s" does not exist' % dir.relative_to(config['public_dir'])
        })
        resp.status_code = httplib.NOT_FOUND
    elif file.startswith('__'):
        resp = jsonify({
            'status': 'client error',
            'message': 'files with double-underscores "__" are protected'
        })
        resp.status_code = httplib.UNAUTHORIZED
    else:
        resp = render_file(dir, file, config)

    return resp

__RENDERERS = od()
__RENDERERS['.md'] = renderers.render_markdown

def add_renderer(extension_with_dot, render_func):
    __RENDERERS[str(extension_with_dot).lower()] = render_func

def render_file(directory, file, config, *args, **kwargs):
    """ Renders the ``file`` located in ``directory`` into a Flask response. """

    # if the file they want exists, just return it
    # UNLESS it's a non-HTML renderable file
    fp = directory.joinpath(file)
    if fp.exists() and (fp.suffix.lower() not in __RENDERERS):
        return send_file(str(directory.joinpath(file)))

    # if it is renderable, render it
    for ext, rfunc in __RENDERERS.items():
        fp = directory.joinpath(file).with_suffix(ext)
        if fp.exists():
            return rfunc(fp, config)

    # if it is the index (and there was none), render the default
    if file == 'index.html':
        return renderers.render_default_index(directory, config)

    resp = jsonify({
        'status': 'client error',
        'message': 'file "%s" does not exist' % directory.joinpath(file).relative_to(config['public_dir'])
    })
    resp.status_code = httplib.UNAUTHORIZED
    return resp