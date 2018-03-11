from flask import jsonify, make_response
from jinja2 import Environment, FileSystemLoader
from mistune import Markdown

from ..util import Path

def text_to_response(source_file, config, body_html, **kwargs):
    # find the template
    if source_file.with_name('__layout.jinja').exists():
        env = Environment(loader=FileSystemLoader(str(source_file.parent)))
    elif Path(config['public_dir']).joinpath('__layout.jinja').exists():
        env = Environment(loader=FileSystemLoader(str(config['public_dir'])))
    else:
        return make_response(body_html, 200)
    template = env.get_template('__layout.jinja')
    return make_response(template.render(body_html=body_html, **kwargs), 200)

def render_markdown(source_file, config, **kwargs):
    """ Renders a Markdown ``source_file`` into an HTML string. """
    rend = Markdown()
    body_html = rend.render(source_file.read_text())
    return text_to_response(source_file, config, body_html, **kwargs)