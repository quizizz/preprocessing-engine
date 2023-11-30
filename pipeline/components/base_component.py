import time
from abc import ABC, abstractmethod

from sanic.log import logger

from pipeline.constants import *
from structures.dto import DTO


class BaseComponent(ABC):
    def __init__(self, *args, **kwargs):
        self.from_key = kwargs.get(FROM_KEY)
        self.to_key = kwargs.get(TO_KEY)

    @abstractmethod
    async def process(self, dto: DTO):
        pass

    async def process_with_timing(self, dto: DTO):
        start_time = time.monotonic()
        result = await self.process(dto)
        logger.info(f"Component {self.__class__.__name__} executed in {(time.monotonic() - start_time) * 1000:.3f} ms")
        return result
