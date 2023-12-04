from structures.dto import DTO
from pipeline.components.base_component import BaseComponent
from utils.preprocessing import composed_preprocessing_function
from pipeline.registry import component_registry
from pipeline.constants import *


@component_registry.register
class BasicPreprocessingComponent(BaseComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = kwargs.get(KEY, TEXT)
        self.processing_function = {"processing_function": kwargs.get("processing_function")}
        self.basic_preprocessor = composed_preprocessing_function(**self.processing_function)

    async def process(self, dto: DTO):
        res = self.basic_preprocessor(dto.get(self.from_key))
        dto.add_additional(self.to_key, res)
        dto.add_additional(PREPROCESSED_TEXT, res)
        return dto
