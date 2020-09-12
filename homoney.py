import argparse
import json

from flask import Flask, render_template


class WrongEnvironment(Exception):
    """Exception raised when wrong environment is set.

    Attributes:
        env -- input environment value which cased exception
        message -- explanation of the error
    """
    def __init__(self, env: str, message: str = 'Wrong environment, options = ["production", "development"]'):
        self.env = env
        self.message = message
        super().__init__(self.message)


def create_app(cfg: dict):
    app = Flask(__name__)
    if cfg['ENV'] == 'development':
        app.config = {
            **app.config,
            'SEND_FILE_MAX_AGE_DEFAULT': 0,
            'TEMPLATES_AUTO_RELOAD': True
        }
    elif cfg['ENV'] == 'production':
        pass
    else:
        raise WrongEnvironment(cfg['ENV'])

    app.config['ENV'] = cfg['ENV']

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/incomes')
    def incomes():
        return {
            'items': [
                {
                    'icon': 'mdi mdi-account',
                    'msg': 'income 1'
                },
                {
                    'icon': 'mdi mdi-account',
                    'msg': 'income 2'
                }
            ]
        }
        
    @app.route('/api/outcomes')
    def outcomes():
        return {
            'items': [
                {
                    'icon': 'mdi mdi-account',
                    'msg': 'outcome 1'
                },
                {
                    'icon': 'mdi mdi-account',
                    'msg': 'outcome 2'
                },
                {
                    'icon': 'mdi mdi-account',
                    'msg': 'outcome 3'
                }
            ]
        }

    app.run(host=cfg['host'], port=cfg['port'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Homoney is an Service for managing your budget')
    parser.add_argument('-c', '--config', type=str, default='cfg.json', help='config filename')

    args = parser.parse_args()
    with open(args.config, 'r') as cfg_file:
        config = json.load(cfg_file)

    create_app(config)
