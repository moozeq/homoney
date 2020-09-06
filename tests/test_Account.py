import unittest

from src.account import Account, months
from src.items import Item, WrongTypeItem


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.acc = Account('John')

    def test_add(self):
        for month in months:
            self.assertEqual(self.acc.balances[month], 0)
            self.acc.add(Item('work', 'in', 1000), month)
            self.assertEqual(self.acc.balances[month], 1000)
            self.acc.add(Item('food', 'out', 250), month)
            self.assertEqual(self.acc.balances[month], 750)
            self.acc.add(Item('food', 'out', 2000), month)
            self.assertEqual(self.acc.balances[month], -1250)
            self.acc.clear(month)
            self.assertEqual(self.acc.balances[month], 0)

    def test_wrong_item(self):
        self.assertRaises(WrongTypeItem, Item,  'food', 'wrong-type', 2000)
