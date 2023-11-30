import yaml
from structures.dto import DTO
from pipeline.registry import component_registry
from pipeline.constants import *

import pipeline.components


class PipelineRunner:
    def __init__(self, config_path):
        self.components = self.load_components(config_path)

    @staticmethod
    def load_components(config_path):
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        components = []
        for component_config in config[COMPONENTS]:
            component_class = component_registry.registry[component_config[NAME]]
            component = component_class(*component_config.get('args', []), **component_config.get('kwargs', {}))
            components.append(component)

        return components

    async def run(self, dto: DTO):
        for component in self.components:
            dto = await component.process_with_timing(dto)
        return dto.to_json()
