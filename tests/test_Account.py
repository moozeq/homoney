import unittest

from src.account import Account, months
from src.items import Item, WrongTypeItem


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.acc = Account('John')

    def tearDown(self) -> None:
        for month in months:
            self.acc.clear()
            self.assertEqual(self.acc.balances[month], 0)

    def test_add(self):
        for month in months:
            self.assertEqual(self.acc.balances[month], 0)
            self.acc.add(Item('work', 'in', 1000, 1), month)
            self.assertEqual(self.acc.balances[month], 1000)
            self.acc.add(Item('food', 'out', 250, 2), month)
            self.assertEqual(self.acc.balances[month], 1000 - 250)
            self.acc.add(Item('food', 'out', 2000, 3), month)
            self.assertEqual(self.acc.balances[month], 1000 - 250 - 2000)

    def test_rm(self):
        for month in months:
            self.acc.add(Item('work', 'in', 1000, 1), month)
            self.acc.add(Item('food', 'out', 250, 2), month)
            self.acc.add(Item('food', 'out', 2000, 3), month)
            self.assertEqual(self.acc.balances[month], 1000 - 250 - 2000)
            self.acc.rm(3, 'out', month)
            self.assertEqual(self.acc.balances[month], 1000 - 250)

    def test_wrong_item(self):
        with self.assertRaises(WrongTypeItem):
            Item('food', 'wrong-type', 2000, 1)
