from typing import Optional

from fspider.utils.middleware import MiddlewareLoader
from fspider.utils.type import Item


class Pipeline:
    async def process_item(self, item: Item) -> Optional[Item]:
        return item


class PipelineManager(MiddlewareLoader):
    name = 'ITEM_PIPELINES'

    async def process_item(self, item: Item) -> Optional[Item]:
        for md in self._middlewares:
            item = await md.process_item(item)
            if not isinstance(item, Item):
                break
        return item
