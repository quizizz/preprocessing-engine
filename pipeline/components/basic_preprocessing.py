from structures.dto import DTO
from pipeline.components.base_component import BaseComponent
from utils.preprocessing import composed_preprocessing_functions
from pipeline.registry import component_registry
from pipeline.constants import *


@component_registry.register
class BasicPreprocessingComponent(BaseComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = kwargs.get(KEY, TEXT)
        self.basic_preprocessor = composed_preprocessing_functions()

    async def process(self, dto: DTO):
        dto.add_additional(self.to_key, self.basic_preprocessor(dto.get(self.from_key)))
        return dto
