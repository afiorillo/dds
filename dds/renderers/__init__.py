import os

from flask import make_response, jsonify
from jinja2 import Environment, FileSystemLoader
from mistune import Markdown
try: from pathlib import Path
except ImportError: from pathlib2 import Path

from ..util import Path

def populate_default_keys(source_file, config, **kwargs):
    sfp = Path(source_file)

    # listdir
    EXCLUDE_FILES = ['favicon.ico', Path(config['static_dir']).name]
    listdir = []
    if sfp.is_file():
        pdir = sfp.parent
    else:
        pdir = sfp
    for oname in os.listdir(str(pdir)):
        fp = pdir.joinpath(oname)
        if fp.name.startswith('__') or fp.name in EXCLUDE_FILES:
            continue
        listdir.append((str(fp.relative_to(Path(config['public_dir'])).as_posix()), fp.name, fp.is_dir()))
    listdir = sorted(listdir, key=lambda tup: tup[2])

    return {'listdir': listdir}


def text_to_response(source_file, config, body_html, **kwargs):
    # look for a template in the current directory, and upward to the root
    layoutFp = source_file.with_name('__layout.jinja')
    while not layoutFp.exists():
        if layoutFp.parent == Path(config['public_dir']):
            resp = jsonify({'status': 'server error', 'message': 'no layout file configured'})
            resp.status_code = 500
            return resp

        layoutFp = layoutFp.parent.parent.joinpath(layoutFp.name)

    env = Environment(loader=FileSystemLoader(str(layoutFp.parent)))

    template = env.get_template('__layout.jinja')
    kwargs.update(populate_default_keys(source_file, config, **kwargs))
    return make_response(template.render(body_html=body_html, **kwargs), 200)


def render_markdown(source_file, config, **kwargs):
    """ Renders a Markdown ``source_file`` into an HTML string. """
    rend = Markdown()
    body_html = rend.render(source_file.read_text())
    return text_to_response(source_file, config, body_html, **kwargs)

def render_default_index(current_dir, config, **kwargs):
    """ Renders the default index file into an HTML string. """
    env = Environment(loader=FileSystemLoader(str(config['public_dir'])))
    template = env.get_template('__default_index.jinja')
    kwargs.update(populate_default_keys(current_dir, config, **kwargs))
    return make_response(template.render(**kwargs), 200)