from typing import Protocol, List

from item import Item


class Updater(Protocol):
    def update_aged_brie(self, item: Item):
        pass

    def update_backstage_passes(self, item: Item):
        pass

    def update_sulfuras(self, item: Item):
        pass

    def update_conjured(self, item: Item):
        pass

    def update_item(self, item: Item):
        pass


class GildedRoseUpdater(Updater):
    def __init__(self, min_quality: int, max_quality: int):
        self.min_quality = min_quality
        self.max_quality = max_quality

    def _determine_item_quality(self, item: Item, modifier=1):
        if modifier >= 0:
            return min(item.quality + modifier, self.max_quality)
        else:  # modifier < 0
            return max(item.quality + modifier, self.min_quality)

    def update_aged_brie(self, item: Item):
        if item.sell_in > 0:
            item.quality = self._determine_item_quality(item, modifier=1)
        else:
            item.quality = self._determine_item_quality(item, modifier=2)
        item.sell_in += -1

    def update_backstage_passes(self, item: Item):
        if item.sell_in > 10:
            item.quality = self._determine_item_quality(item)
        elif item.sell_in > 5:
            item.quality = self._determine_item_quality(item, modifier=2)
        elif item.sell_in > 0:
            item.quality = self._determine_item_quality(item, modifier=3)
        else:
            item.quality = 0

        item.sell_in += -1

    def update_sulfuras(self, item: Item):
        pass

    def update_conjured(self, item: Item):
        if item.sell_in > 0:
            item.quality = self._determine_item_quality(item, modifier=-2)
        else:
            item.quality = self._determine_item_quality(item, modifier=-4)

        item.sell_in += -1

    def update_item(self, item: Item):
        if item.sell_in > 0:
            item.quality = self._determine_item_quality(item, modifier=-1)
        else:
            item.quality = self._determine_item_quality(item, modifier=-2)
        item.sell_in += -1


class GildedRose:
    def __init__(self, updater: Updater):
        self.updater = updater

    def update_quality(self, items: List[Item]):
        for item in items:
            if item.name == 'Aged Brie':
                self.updater.update_aged_brie(item)
            elif item.name == 'Backstage passes to a TAFKAL80ETC concert':
                self.updater.update_backstage_passes(item)
            elif item.name == 'Sulfuras, Hand of Ragnaros':
                self.updater.update_sulfuras(item)
            elif item.name == 'Conjured Mana Cake':
                self.updater.update_conjured(item)
            else:
                self.updater.update_item(item)
