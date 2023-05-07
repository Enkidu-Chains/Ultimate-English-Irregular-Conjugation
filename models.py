from enum import  StrEnum
import genanki

from common import UEICModel


class UEICNote(genanki.Note):
    def __init__(self, model = UEICModel, fields = None, sort_field = None, tags = None, guid = None, due = 0):
        super().__init__(model, fields, sort_field, tags, guid, due)


class TypeOfCard(StrEnum):
    INFINITIVE = "infinitive"
    PAST_TENSE = "past_tense"
    PAST_PARTICIPLE = "past_participle"
    
    
class TypeOfVerb(StrEnum):
    SAME_SAME_SAME = "same-same-same"
    DIF_SAME_SAME = "dif-same-same"
    DIF_DIF_DIF = "dif-dif-dif"


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
    
    def get_type_of_verb(self) -> TypeOfVerb:
        if self.infinitive == "be":
            return TypeOfVerb.DIF_DIF_DIF
        
        if isinstance(self.past_tense, list) and isinstance(self.past_participle, list):
            if self.infinitive == self.past_tense[0] and self.infinitive == self.past_participle[0]:
                return TypeOfVerb.SAME_SAME_SAME
            
            if self.past_tense[0] == self.past_participle[0]:
                return TypeOfVerb.DIF_SAME_SAME

            return TypeOfVerb.DIF_DIF_DIF
        else:
            if self.infinitive == self.past_tense and self.infinitive == self.past_participle:
                return TypeOfVerb.SAME_SAME_SAME
            
            if self.past_tense == self.past_participle:
                return TypeOfVerb.DIF_SAME_SAME

            return TypeOfVerb.DIF_DIF_DIF
