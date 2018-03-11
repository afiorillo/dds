from json import load, dump
from pathlib2 import Path

DEFAULT_CONFIG_FILE = '~/.dds/config.json'

DEFAULT_CONFIG = {
    'bind_ip': '0.0.0.0',
    'bind_port': 8001,
}

def get_config(config_filepath=DEFAULT_CONFIG_FILE, write_immediately=True):
    fp = Path(config_filepath).resolve()
    cfg = DEFAULT_CONFIG.copy()
    with fp.open('rb') as fIn:
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
    with fp.open('wb') as fOut:
        dump(config, fOut)
    return fp