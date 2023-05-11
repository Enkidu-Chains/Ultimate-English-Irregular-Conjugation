class StoredVerb:
    infinitive: str
    present_tense: str | list[str]
    past_tense: str | list[str]
    past_participle: str | list[str]
    infinitive_reading: str
    present_tense_reading: str | list[str]
    past_tense_reading: str | list[str]
    past_participle_reading: str | list[str]
    context: str
    translation: str | list[str]
    infinitive_uuid: str | list[str]
    past_tense_uuid: str | list[str]
    past_participle_uuid: str

    def __init__(self, values: dict) -> None:
        self.__dict__ = values
