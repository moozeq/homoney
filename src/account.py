from typing import Dict, List

from src.items import Item

months = {
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
}


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

    @property
    def outcomes(self) -> Dict[str, int]:
        return {
            month: sum(outcome.value for outcome in self._outcomes_items[month])
            for month in months
        }

    @property
    def incomes(self) -> Dict[str, int]:
        return {
            month: sum(income.value for income in self._incomes_items[month])
            for month in months
        }

    @property
    def balances(self) -> Dict[str, int]:
        return {
            month: self.incomes[month] - self.outcomes[month]
            for month in months
        }

    def add(self, item: Item, month: str):
        items = self._items[item.type][month]
        items.append(item)

    def clear(self, month: str):
        for items_type in ['in', 'out']:
            items = self._items[items_type][month]
            items.clear()
