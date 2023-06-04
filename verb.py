from typing import Callable

from enums import AnkiNoteType, TobePastTemseForms, TobePresentTenseForms, VerbType
from stored_verb import StoredVerb
from templates.note_templates import NoteTemplates
from templates.prompt_templates import PromptTemplates
from templates.tobe_prompt_templates import TobePromptTemplates
from ueic_note import UEICNote


class Word:
    spelling: str
    reading: str

    def __init__(self, spelling: str, reading: str) -> None:
        self.spelling = spelling
        self.reading = reading


class Verb:
    infinitive: Word
    present_tense: Word | list[Word]
    past_tense: Word | list[Word]
    regular_past_tense: Word | None = None
    past_participle: Word
    regular_past_participle: Word | None = None
    context: str
    translation: str
    infinitive_uuid: str | list[str]
    past_tense_uuid: str | list[str]
    past_participle_uuid: str

    def __init__(self, verb: StoredVerb) -> None:
        self.__set_infinitive(verb.infinitive, verb.infinitive_reading)
        self.__set_present_tense(
            verb.present_tense, verb.present_tense_reading)
        self.__set_past_tense(verb.past_tense, verb.past_tense_reading)
        self.__set_past_participle(
            verb.past_participle, verb.past_participle_reading)
        self.__set_context(verb.context)
        self.__set_translation(verb.translation)
        self.__set_uuids(verb.infinitive_uuid, verb.past_tense_uuid, verb.past_participle_uuid)

    @property
    def anki_notes(self) -> list[UEICNote]:
        if self.is_tobe:
            return self.__get_anki_tobe_notes()
        else:
            return self.__get_anki_notes()

    @property
    def is_tobe(self) -> bool:
        return self.infinitive.spelling == "be"

    @property
    def verb_type(self) -> VerbType:
        if self.is_tobe:
            return VerbType.DIF_DIF_DIF

        if self.infinitive.spelling == self.past_tense.spelling and self.infinitive.spelling == self.past_participle.spelling:
            return VerbType.SAME_SAME_SAME

        if self.past_tense.spelling == self.past_participle.spelling:
            return VerbType.DIF_SAME_SAME

        return VerbType.DIF_DIF_DIF

    def __get_anki_notes(self) -> list[UEICNote]:
        return [
            self.__create_infinitive_note(),
            self.__create_past_tense_note(),
            self.__create_past_participle_note()
        ]

    def __get_anki_tobe_notes(self) -> list[UEICNote]:
        return [
            self.__create_infinitive_tobe_note(TobePresentTenseForms.AM),
            self.__create_infinitive_tobe_note(TobePresentTenseForms.IS),
            self.__create_infinitive_tobe_note(TobePresentTenseForms.ARE),
            self.__create_past_tense_tobe_note(TobePastTemseForms.WAS),
            self.__create_past_tense_tobe_note(TobePastTemseForms.WERE),
            self.__create_past_participle_tobe_note()
        ]

    def __set_infinitive(self, spelling: str, reading: str) -> None:
        self.infinitive = Word(spelling, reading)

    def __set_present_tense(self, spelling: str | list[str], reading: str | list[str]) -> None:
        if (str(TobePresentTenseForms.AM) in spelling and
                str(TobePresentTenseForms.IS) in spelling and
                str(TobePresentTenseForms.ARE) in spelling):
            self.present_tense = [Word(spelling[i], reading[i])
                                  for i in range(len(spelling))]
        else:
            self.present_tense = Word(spelling, reading)

    def __set_past_tense(self, spelling: str | list[str], reading: str | list[str]) -> None:
        if (str(TobePastTemseForms.WAS) in spelling and
                str(TobePastTemseForms.WERE) in spelling):
            self.past_tense = [Word(spelling[i], reading[i])
                               for i in range(len(spelling))]
        elif isinstance(spelling, list):
            self.past_tense = Word(spelling[0], reading=reading[0])
            self.regular_past_tense = Word(spelling[1], reading[1])
        else:
            self.past_tense = Word(spelling, reading)

    def __set_past_participle(self, spelling: str | list[str], reading: str | list[str]) -> None:
        if isinstance(spelling, list):
            self.past_participle = Word(spelling[0], reading[0])
            self.regular_past_participle = Word(spelling[1], reading[1])
        else:
            self.past_participle = Word(spelling, reading)

    def __set_context(self, context: str) -> None:
        self.context = context

    def __set_translation(self, translation: str | list[str]) -> None:
        if isinstance(translation, list):
            translation: str = ", ".join(translation)

        self.translation = translation

    def __set_uuids(self, infinitive: str | list[str], past_tense: str | list[str], past_participle: str) -> None:
        self.infinitive_uuid = infinitive
        self.past_tense_uuid = past_tense
        self.past_participle_uuid = past_participle

    def __create_infinitive_note(self) -> UEICNote:
        uuid: str = self.infinitive_uuid
        prompt: str = PromptTemplates.infinitive(
            self.infinitive.spelling, self.present_tense.spelling, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.spelling, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.present_tense.spelling, self.present_tense.reading),
            NoteTemplates.ua_dictionary(self.infinitive.spelling)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.INFINITIVE, self.infinitive.spelling]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_tense_note(self) -> UEICNote:
        uuid: str = self.past_tense_uuid
        prompt: str = PromptTemplates.past_tense(
            self.infinitive.spelling, self.past_tense.spelling, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.spelling, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_tense.spelling, self.past_tense.reading),
            (NoteTemplates.regular_conjugation_with_reading(self.regular_past_tense.spelling,
                                                            self.regular_past_tense.reading) if self.regular_past_tense != None else ""),
            NoteTemplates.ua_dictionary(self.infinitive.spelling)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_TENSE, self.infinitive.spelling]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_participle_note(self) -> UEICNote:
        uuid: str = self.past_participle_uuid
        prompt: str = PromptTemplates.past_participle(
            self.infinitive.spelling, self.past_participle.spelling, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.spelling, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_participle.spelling, self.past_participle.reading),
            (NoteTemplates.regular_conjugation_with_reading(self.regular_past_participle.spelling,
                                                            self.regular_past_participle.reading) if self.regular_past_tense != None else ""),
            NoteTemplates.ua_dictionary(self.infinitive.spelling)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_PARTICIPLE, self.infinitive.spelling]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_infinitive_tobe_note(self, tobe_form: TobePresentTenseForms) -> UEICNote:
        i: int = [self.present_tense.index(
            form) for form in self.present_tense if form.spelling == str(tobe_form)][0]
        tobe_prompt: Callable[[str, str, str], str]

        if tobe_form == TobePresentTenseForms.AM:
            tobe_prompt = TobePromptTemplates.infinitive_am
        if tobe_form == TobePresentTenseForms.IS:
            tobe_prompt = TobePromptTemplates.infinitive_is
        if tobe_form == TobePresentTenseForms.ARE:
            tobe_prompt = TobePromptTemplates.infinitive_are

        uuid: str = self.infinitive_uuid[i]
        prompt: str = tobe_prompt(
            self.infinitive.spelling, self.present_tense[i].spelling, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.spelling, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.present_tense[i].spelling, self.present_tense[i].reading),
            NoteTemplates.ua_dictionary(self.infinitive.spelling)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.INFINITIVE, self.infinitive.spelling]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_tense_tobe_note(self, tobe_form: TobePastTemseForms) -> UEICNote:
        i: int = [self.past_tense.index(
            form) for form in self.past_tense if form.spelling == str(tobe_form)][0]
        tobe_prompt: Callable[[str, str, str], str]

        if tobe_form == TobePastTemseForms.WAS:
            tobe_prompt = TobePromptTemplates.past_tense_was
        if tobe_form == TobePastTemseForms.WERE:
            tobe_prompt = TobePromptTemplates.past_tense_were

        uuid: str = self.past_tense_uuid[i]
        prompt: str = tobe_prompt(
            self.infinitive.spelling, self.past_tense[i].spelling, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.spelling, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_tense[i].spelling, self.past_tense[i].reading),
            NoteTemplates.ua_dictionary(self.infinitive.spelling)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_TENSE, self.infinitive.spelling]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_participle_tobe_note(self) -> UEICNote:
        uuid: str = self.past_participle_uuid
        prompt: str = TobePromptTemplates.past_participle(
            self.infinitive.spelling, self.past_participle.spelling, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.spelling, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_participle.spelling, self.past_participle.reading),
            NoteTemplates.ua_dictionary(self.infinitive.spelling)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_PARTICIPLE, self.infinitive.spelling]

        return UEICNote.create(uuid, prompt, notes, tags)
