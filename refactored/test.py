import unittest
from typing import List

from gilded_rose import GildedRose, Item, GildedRoseUpdater


class GildedRoseTest(unittest.TestCase):

    def _simulate(self, items: List[Item], times=1):
        for i in range(times):
            self.gilded_rose.update_quality(items)

    def setUp(self):
        self.gilded_rose = GildedRose(updater=GildedRoseUpdater(min_quality=0, max_quality=50))

    def test_normal_item(self):
        # Set up the item
        item = Item("+5 Dexterity Vest", 10, 20)

        # One day after
        self._simulate([item])
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 19)

        # Sell by date passed
        self._simulate([item], item.sell_in + 1)
        self.assertEqual(item.sell_in, -1)

        # Quality degrades twice as fast now
        self.assertEqual(item.quality, 8)
        self._simulate([item], 10)
        self.assertEqual(item.sell_in, -11)
        self.assertEqual(item.quality, 0)  # never be less than 0

    def test_aged_brie(self):
        # Set up the item
        item = Item("Aged Brie", 10, 20)

        # One day after
        self._simulate([item])
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 21)

        # Sell by date passed
        self._simulate([item], item.sell_in + 1)
        self.assertEqual(item.sell_in, -1)

        # Quality increases twice as fast now
        self.assertEqual(item.quality, 32)
        self._simulate([item], 10)
        self.assertEqual(item.sell_in, -11)
        self.assertEqual(item.quality, 50)

    def test_sulfuras(self):
        # Set up the item
        item = Item("Sulfuras, Hand of Ragnaros", 20, 80)

        # One day after
        self._simulate([item])
        self.assertNotEqual(item.sell_in, 19)
        self.assertEqual(item.sell_in, 20)
        self.assertEqual(item.quality, 80)

        # sell by date passed
        self._simulate([item], item.sell_in + 1)
        self.assertEqual(item.sell_in, 20)
        self.assertNotEqual(item.sell_in, -1)

    def test_backstage_passes(self):
        # Set up the item
        item = Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)

        # One day after
        self._simulate([item])
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 21)

        # Sell in 10 or less
        self._simulate([item], 9)
        self.assertEqual(item.sell_in, 10)
        self.assertEqual(item.quality, 30)

        self._simulate([item])
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 32)

        # Sell in 5 or less
        self._simulate([item], 4)
        self.assertEqual(item.sell_in, 5)
        self.assertEqual(item.quality, 40)

        self._simulate([item])
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 43)

        self._simulate([item], 2)
        self.assertEqual(item.sell_in, 2)
        self.assertEqual(item.quality, 49)

        # Never gets beyond 50 and drops to 0 once sell in passed
        self._simulate([item])
        self.assertEqual(item.sell_in, 1)
        self.assertEqual(item.quality, 50)

        self._simulate([item], 2)
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 0)

    def test_conjured(self):
        # Set up the item
        item = Item("Conjured Mana Cake", 20, 50)

        # One day after
        self._simulate([item])
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 48)

        # sell by date passed -- will decrease twice as fast as normal items (-4)
        self._simulate([item], item.sell_in + 1)
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 6)

        self._simulate([item])
        self.assertEqual(item.sell_in, -2)
        self.assertEqual(item.quality, 2)

        self._simulate([item])
        self.assertEqual(item.sell_in, -3)
        self.assertEqual(item.quality, 0)


if __name__ == '__main__':
    unittest.main()