import argparse
import json

from flask import Flask


def create_app(cfg: dict):
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Gimme gimme gimme money'

    app.run(host=cfg['host'], port=cfg['port'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Homoney is an Service for managing your budget')
    parser.add_argument('-c', '--config', type=str, default='cfg.json', help='config filename')

    args = parser.parse_args()
    with open(args.config, 'r') as cfg_file:
        config = json.load(cfg_file)

    create_app(config)
