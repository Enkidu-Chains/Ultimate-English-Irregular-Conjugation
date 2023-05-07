from enum import Enum
import genanki

from common import UEICModel


class UEICNote(genanki.Note):
    def __init__(self, model = UEICModel, fields = None, sort_field = None, tags = None, guid = None, due = 0):
        super().__init__(model, fields, sort_field, tags, guid, due)

    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


class Verb:
    infinitive: str
    present_tense: str | list[str]
    past_tense: str | list[str]
    past_participle: str | list[str]
    infinitive_reading: str
    present_tense_reading: str | list[str]
    past_tense_reading: str | list[str]
    past_participle_reading: str | list[str]
    context: str
    translation: str

    def __init__(self, values: dict) -> None:
        self.__dict__ = values


class TypeOfCard(Enum):
    INFINITIVE = 1
    PAST_TENSE = 2
    PAST_PARTICIPLE = 3