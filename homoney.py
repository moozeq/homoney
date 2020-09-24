#!/usr/bin/env python3

import argparse
import json

from flask import Flask, render_template, request
from src.account import Account
from src.items import WrongTypeItem, WrongItem, Item
from src.items import incomes as available_incomes, outcomes as available_outcomes


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

    acc_name = '1337'
    acc = Account(acc_name)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/incomes')
    def incomes():
        return {
            'items': acc.get_comes('in', 'web')['JAN']
        }
        
    @app.route('/api/outcomes')
    def outcomes():
        return {
            'items': acc.get_comes('out', 'web')['JAN']
        }

    @app.route('/api/balance')
    def balance():
        return {
            'income': acc.get_comes('in', 'value')['JAN'],
            'outcome': acc.get_comes('out', 'value')['JAN'],
            'balance': acc.balances['JAN'],
            'currency': '$'
        }

    @app.route('/api/available')
    def available():
        return {
            'in': [
                {
                    'value': come_name,
                    'text': available_incomes[come_name]['desc'],
                    'icon': available_incomes[come_name]['icon'],
                } for come_name in available_incomes
            ],
            'out': [
                {
                    'value': come_name,
                    'text': available_outcomes[come_name]['desc'],
                    'icon': available_outcomes[come_name]['icon'],
                } for come_name in available_outcomes
            ]
        }

    @app.route('/api/save', methods=['POST'])
    def save():
        acc.save()
        return {'success': True}, 200, {'ContentType': 'application/json'}

    @app.route('/api/load', methods=['POST'])
    def load():
        nonlocal acc
        acc = Account.load(f'data/{acc_name}.pickle')
        return {'success': True}, 200, {'ContentType': 'application/json'}

    @app.route('/api/clear', methods=['POST'])
    def clear():
        acc.clear()
        return {'success': True}, 200, {'ContentType': 'application/json'}

    @app.route('/api/add', methods=['POST'])
    def add():
        data = request.get_json()
        item: Item = acc.add(data, data['date']['month'])

        if not item:
            raise WrongItem(f'Item could not be add')

        if item.type == 'in':
            return item.web_data
        elif item.type == 'out':
            return item.web_data
        else:
            raise WrongTypeItem(f'Wrong item type: {item.type}')

    @app.route('/api/rm', methods=['POST'])
    def rm():
        data = request.get_json()
        deleted = acc.rm(data['id'], data['type'], data['date']['month'])
        return {'success': deleted}, 200, {'ContentType': 'application/json'}

    app.run(host=cfg['host'], port=cfg['port'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Homoney is an Service for managing your budget')
    parser.add_argument('-c', '--config', type=str, default='cfg.json', help='config filename')

    args = parser.parse_args()
    with open(args.config, 'r') as cfg_file:
        config = json.load(cfg_file)

    create_app(config)
