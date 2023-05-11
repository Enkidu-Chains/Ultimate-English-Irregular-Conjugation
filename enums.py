from enum import StrEnum


class AnkiNoteType(StrEnum):
    INFINITIVE = "infinitive"
    PAST_TENSE = "past_tense"
    PAST_PARTICIPLE = "past_participle"


class VerbType(StrEnum):
    SAME_SAME_SAME = "same-same-same"
    DIF_SAME_SAME = "dif-same-same"
    DIF_DIF_DIF = "dif-dif-dif"


class TobePresentTenseForms(StrEnum):
    AM = "am"
    IS = "is"
    ARE = "are"


class TobePastTemseForms(StrEnum):
    WAS = "was"
    WERE = "were"
