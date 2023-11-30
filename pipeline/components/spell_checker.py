import importlib.resources as pkg_resources
from sanic.log import logger
from symspellpy import SymSpell

from pipeline.registry import component_registry
from structures.dto import DTO
from .base_component import BaseComponent


@component_registry.register
class SpellCheckerComponent(BaseComponent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sym_spell = SymSpell(**kwargs.get("init_kwargs", {}))

        self.spell_correction_kwargs = kwargs.get("spell_correction_kwargs", {})
        self.load_dictionaries()

    def load_dictionaries(self):
        try:
            with (
                pkg_resources.path(
                    "symspellpy",
                    "frequency_dictionary_en_82_765.txt"
                ) as dictionary_path,
                pkg_resources.path(
                    "symspellpy",
                    "frequency_bigramdictionary_en_243_342.txt"
                ) as bigram_path
            ):
                self.sym_spell.load_dictionary(str(dictionary_path), term_index=0, count_index=1)
                self.sym_spell.load_bigram_dictionary(str(bigram_path), term_index=0, count_index=2)
        except Exception as e:
            logger.error(f"Error in loading dictionaries: {e}")
            raise Exception(f"Error in init {self.__class__.__name__}")

    async def process(self, dto: DTO):
        input_text = dto.get(self.from_key)
        suggestions = self.sym_spell.lookup_compound(input_text, max_edit_distance=2)
        if any([suggestion.term != input_text for suggestion in suggestions]):
            logger.error(f"SPELLING MISTAKE: {input_text}")
        dto.add_additional(self.to_key, " ".join([suggestion.term for suggestion in suggestions]))
        return dto
