import argparse
from shutil import copytree

try: from pathlib import Path
except ImportError: from pathlib2 import Path

from .config import DEFAULT_CONFIG, write_config

DEFAULT_SITES = Path(__file__).parent.joinpath('default_site')

def main():
    parser = argparse.ArgumentParser(
        description='Bootstrap a server configuration and default templates.'
    )
    parser.add_argument('server_directory', help='Path to a directory that does NOT exist. '
                                                 'Will create server files here.')
    # TODO: other arguments
    args = parser.parse_args()

    # make the directory
    dir = Path(args.server_directory)
    dir.mkdir(parents=True, exist_ok=False)

    # write the default templates
    pubDir = dir.joinpath('public')
    # pubDir.mkdir(exist_ok=False)
    copytree(str(DEFAULT_SITES), str(pubDir))

    # write the config
    cfg = DEFAULT_CONFIG.copy()
    cfg['config_file'] = dir.joinpath('server_config.json')
    cfg['public_dir'] = pubDir
    cfg['static_dir'] = pubDir.joinpath('static')
    write_config(cfg)

if __name__ == '__main__':
    main()