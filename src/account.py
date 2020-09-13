from typing import Dict, List, Union

from src.items import Item

months = {
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
}


class WrongComeType(Exception):
    pass


class Account:
    """
    Main class containing all expenses and incomes items and allowing access to
    expenses, incomes and balances for 12 months.
    """
    def __init__(self, name: str):
        self.name = name
        self._outcomes_items: Dict[str, List[Item]] = {month: [] for month in months}
        self._incomes_items: Dict[str, List[Item]] = {month: [] for month in months}
        self._items = {
            'in': self._incomes_items,
            'out': self._outcomes_items
        }

    def get_comes(self, come_type: str, data_type: str) -> Dict[str, Union[int, List[Item], List[dict]]]:
        """
        Get comes based on type:
            - 'value':  value of outcome
            - 'items':  Item objects
            - 'web':    web dictionary
        """
        if come_type == 'in':
            items = self._incomes_items
        elif come_type == 'out':
            items = self._outcomes_items
        else:
            raise WrongComeType(f'Wrong come type provided: {come_type}')

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
                month: [item.web_data for item in items[month]]
                for month in months
            }
        else:
            raise WrongComeType(f'Wrong data type provided: {data_type}')

    @property
    def balances(self) -> Dict[str, int]:
        return {
            month: self.get_comes('in', 'value')[month] - self.get_comes('out', 'value')[month]
            for month in months
        }

    def add(self, item: Item, month: str):
        items = self._items[item.type][month]
        items.append(item)
        
    def clear(self, month: str):
        for items_type in ['in', 'out']:
            items = self._items[items_type][month]
            items.clear()
