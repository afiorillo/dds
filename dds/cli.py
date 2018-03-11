import argparse
from server import run_server

def main():
    parser = argparse.ArgumentParser(
        description='A dynamic documentation server'
    )
    parser.add_argument('--config-file', default=None)
    # TODO: other arguments
    args = parser.parse_args()

    app = run_server(config_file=args.config_file)