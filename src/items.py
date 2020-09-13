import json

with open('data/outcomes.json', 'r') as exp_json:
    outcomes = json.load(exp_json)
with open('data/incomes.json', 'r') as inc_json:
    incomes = json.load(inc_json)

currency = '$'


class WrongTypeItem(Exception):
    pass


class Item:
    def __init__(self, name: str, item_type: str, value: float = 0.0):
        self.name = name
        self.value = value
        self.type = item_type

        if item_type == 'in' and name in incomes:
            item_data = incomes[name]
        elif item_type == 'out' and name in outcomes:
            item_data = outcomes[name]
        else:
            if item_type in ['in', 'out']:
                raise WrongTypeItem(f'Item name = {name}, not corresponding to item type = {item_type}')
            else:
                raise WrongTypeItem(f'Wrong item type: {item_type}')

        self.data = item_data

    @property
    def web_data(self):
        return {
            **self.data,
            'name': self.name,
            'value': self.value,
            'currency': currency,
        }

    def add(self, value_to_add: float):
        self.value += value_to_add

    def mul(self, value_to_mul: float):
        self.value *= value_to_mul
