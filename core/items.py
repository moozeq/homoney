import json

with open('../data/outcomes.json', 'r') as exp_json:
    outcomes = json.load(exp_json)
with open('../data/incomes.json', 'r') as inc_json:
    incomes = json.load(inc_json)


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
            raise WrongTypeItem

        self.desc = item_data['desc']

    def add(self, value_to_add: float):
        self.value += value_to_add

    def mul(self, value_to_mul: float):
        self.value *= value_to_mul
