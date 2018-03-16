from json import load, dumps
try: from pathlib import PurePath
except ImportError: from pathlib2 import PurePath
import six

from .util import Path

DEFAULT_CONFIG_FILE = Path('~/.dds/config.json')

DEFAULT_CONFIG = {
    'bind_ip': '127.0.0.1',
    'bind_port': 8001,
    'public_dir': Path('~/.dds/public'),
    'static_dir': Path('~/.dds/public/static'),
}

def get_config(config_filepath=DEFAULT_CONFIG_FILE, write_immediately=True):
    if config_filepath == DEFAULT_CONFIG_FILE:
        # make sure it exists
        DEFAULT_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not DEFAULT_CONFIG_FILE.exists():
            with DEFAULT_CONFIG_FILE.open('wb') as fOut:
                fOut.write('{}')

    fp = Path(config_filepath).resolve()
    cfg = DEFAULT_CONFIG.copy()
    with fp.open('r') as fIn:
        cfg.update(load(fIn))
    cfg['config_file'] = str(fp)

    if write_immediately:
        write_config(cfg)

    return cfg


def write_config(config):
    try:
        fp = Path(config['config_file'])
    except KeyError:
        raise ValueError('Configuration missing required key: "config_file"')

    for k, v in config.items():
        # write out paths as strings to keep JSON happy
        if isinstance(v, PurePath):
            config[k] = str(v)

    with fp.open('w') as fOut:
        fOut.write(six.u(dumps(config, indent=2)))
    return fp