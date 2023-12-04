import re
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
        self.spell_correction_kwargs = kwargs.get(
            "spell_correction_kwargs",
            {
                "ignore_term_with_digits": True,
                "ignore_non_words": True,
                "max_edit_distance": 2,
            }
        )
        self.CORRECTED_TEXT = "corrected_text"
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
                ) as bigram_path,
            ):
                self.sym_spell.load_dictionary(str(dictionary_path), term_index=0, count_index=1)
                self.sym_spell.load_bigram_dictionary(str(bigram_path), term_index=0, count_index=2)
        except Exception as e:
            logger.error(f"Error in loading dictionaries: {e}")
            raise Exception(f"Error in init {self.__class__.__name__}")

    def get_corrected_text(self, text):
        # Regular expression to identify non-digit segments
        pattern = r"(?:\b|\D)\d+[\d-]*\b"
        corrected_text = []
        last_index = 0

        for match in re.finditer(pattern, text):
            start, end = match.span()
            non_digit_segment = text[last_index:start]
            if non_digit_segment:
                suggestions = self.sym_spell.lookup_compound(non_digit_segment, **self.spell_correction_kwargs)
                corrected_segment = suggestions[0].term if suggestions else non_digit_segment
                corrected_text.append(corrected_segment)
            corrected_text.append(text[start:end])
            last_index = end

        final_segment = text[last_index:]
        if final_segment:
            suggestions = self.sym_spell.lookup_compound(final_segment, **self.spell_correction_kwargs)
            corrected_text.append(suggestions[0].term if suggestions else final_segment)

        return "".join(corrected_text)

    async def process(self, dto: DTO):
        input_text = dto.get(self.from_key)
        corrected_text = self.get_corrected_text(input_text)
        dto.add_additional(self.CORRECTED_TEXT, corrected_text)
        dto.add_additional(self.to_key, corrected_text)
        return dto
