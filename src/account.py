import json
import pickle
from typing import Dict, List, Union, Optional

from src.items import Item

months = {
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
}


class WrongDataType(Exception):
    pass


class Account:
    """
    Main class containing all expenses and incomes items and allowing access to
    expenses, incomes and balances for 12 months.
    """
    def __init__(self, name: str):
        self.name = name
        self.filename = f'data/{self.name}.pickle'
        self.items_cnt = 0
        self._items: Dict[str, Dict[str, List[Item]]] = {
            'in': {month: [] for month in months},
            'out': {month: [] for month in months}
        }

    def get_comes(self, come_type: str, data_type: str) -> Dict[str, Union[int, List[Item], List[dict]]]:
        """
        Get comes based on type:
            - 'value':  value of outcome
            - 'items':  Item objects
            - 'web':    web dictionary
        """
        if come_type == 'in':
            items = self._items['in']
        elif come_type == 'out':
            items = self._items['out']
        else:
            raise WrongDataType(f'Wrong come type provided: {come_type}')

        if data_type == 'value':
            return {
                month: sum(outcome.value for outcome in items[month])
                for month in months
            }
        elif data_type == 'items':
            return {
                month: items[month]
                for month in months
            }
        elif data_type == 'web':
            return {
                month: {item.id: item.web_data for item in items[month]}
                for month in months
            }
        else:
            raise WrongDataType(f'Wrong data type provided: {data_type}')

    @property
    def balances(self) -> Dict[str, int]:
        return {
            month: self.get_comes('in', 'value')[month] - self.get_comes('out', 'value')[month]
            for month in months
        }

    def add(self, item: Union[Item, dict], month: str) -> Optional[Item]:
        if isinstance(item, Item):
            pass
        elif isinstance(item, dict):
            item = Item(item['name'], item['item_type'], item['value'], self.items_cnt)
        else:
            raise WrongDataType(f'Wrong item type, available = [Item, dict]; passed = {type(item)}')

        items = self._items[item.type][month]
        # TODO check if no item with same id
        items.append(item)
        self.items_cnt += 1
        return item

    def rm(self, item_id: int, item_type: str, month: str) -> bool:
        prev_len = len(self._items[item_type][month])
        self._items[item_type][month] = [item for item in self._items[item_type][month] if item.id != item_id]
        cur_len = len(self._items[item_type][month])
        return True if prev_len - cur_len > 0 else False
        
    def clear(self):
        for items_type in ['in', 'out']:
            for month in months:
                items = self._items[items_type][month]
                items.clear()

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(filename: str) -> 'Account':
        with open(filename, 'rb') as file:
            return pickle.load(file)
