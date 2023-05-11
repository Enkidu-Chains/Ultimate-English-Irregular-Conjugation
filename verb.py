from typing import Callable

from stored_verb import StoredVerb
from enums import AnkiNoteType, TobePastTemseForms, TobePresentTenseForms, VerbType
from templates.prompt_templates import PromptTemplates
from templates.note_templates import NoteTemplates
from templates.tobe_prompt_templates import TobePromptTemplates
from ueic_note import UEICNote


class Word:
    word: str
    reading: str

    def __init__(self, word: str, reading: str) -> None:
        self.word = word
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
        return self.infinitive.word == "be"

    @property
    def verb_type(self) -> VerbType:
        if self.is_tobe:
            return VerbType.DIF_DIF_DIF

        if self.infinitive.word == self.past_tense.word and self.infinitive.word == self.past_participle.word:
            return VerbType.SAME_SAME_SAME

        if self.past_tense.word == self.past_participle.word:
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

    def __set_infinitive(self, infinitive: str, reading: str) -> None:
        self.infinitive = Word(infinitive, reading)

    def __set_present_tense(self, present_tense: str | list[str], reading: str | list[str]) -> None:
        if (str(TobePresentTenseForms.AM) in present_tense and
            str(TobePresentTenseForms.IS) in present_tense and
            str(TobePresentTenseForms.ARE) in present_tense):
            self.present_tense = [Word(present_tense[i], reading[i])
                                  for i in range(len(present_tense))]
        else:
            self.present_tense = Word(present_tense, reading)

    def __set_past_tense(self, past_tense: str | list[str], reading: str | list[str]) -> None:
        if (str(TobePastTemseForms.WAS) in past_tense and
            str(TobePastTemseForms.WERE) in past_tense):
            self.past_tense = [Word(past_tense[i], reading[i])
                               for i in range(len(past_tense))]
        elif isinstance(past_tense, list):
            self.past_tense = Word(past_tense[0], reading= reading[0])
            self.regular_past_tense = Word(past_tense[1], reading[1])
        else:
            self.past_tense = Word(past_tense, reading)

    def __set_past_participle(self, past_participle: str | list[str], reading: str | list[str]) -> None:
        if isinstance(past_participle, list):
            self.past_participle = Word(past_participle[0], reading[0])
            self.regular_past_participle = Word(past_participle[1], reading[1])
        else:
            self.past_participle = Word(past_participle, reading)

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
            self.infinitive.word, self.present_tense.word, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.word, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.present_tense.word, self.present_tense.reading),
            NoteTemplates.ua_dictionary(self.infinitive.word)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.INFINITIVE, self.infinitive.word]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_tense_note(self) -> UEICNote:
        uuid: str = self.past_tense_uuid
        prompt: str = PromptTemplates.past_tense(
            self.infinitive.word, self.past_tense.word, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.word, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_tense.word, self.past_tense.reading),
            (NoteTemplates.regular_conjugation_with_reading(self.regular_past_tense.word,
             self.regular_past_tense.reading) if self.regular_past_tense != None else ""),
            NoteTemplates.ua_dictionary(self.infinitive.word)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_TENSE, self.infinitive.word]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_participle_note(self) -> UEICNote:
        uuid: str = self.past_participle_uuid
        prompt: str = PromptTemplates.past_participle(
            self.infinitive.word, self.past_participle.word, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.word, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_participle.word, self.past_participle.reading),
            (NoteTemplates.regular_conjugation_with_reading(self.regular_past_participle.word,
             self.regular_past_participle.reading) if self.regular_past_tense != None else ""),
            NoteTemplates.ua_dictionary(self.infinitive.word)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_PARTICIPLE, self.infinitive.word]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_infinitive_tobe_note(self, tobe_form: TobePresentTenseForms) -> UEICNote:
        i: int = [self.present_tense.index(
            form) for form in self.present_tense if form.word == str(tobe_form)][0]
        tobe_prompt: Callable[[str, str, str], str]

        if tobe_form == TobePresentTenseForms.AM:
            tobe_prompt = TobePromptTemplates.infinitive_am
        if tobe_form == TobePresentTenseForms.IS:
            tobe_prompt = TobePromptTemplates.infinitive_is
        if tobe_form == TobePresentTenseForms.ARE:
            tobe_prompt = TobePromptTemplates.infinitive_are

        uuid: str = self.infinitive_uuid[i]
        prompt: str = tobe_prompt(
            self.infinitive.word, self.present_tense[i].word, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.word, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.present_tense[i].word, self.present_tense[i].reading),
            NoteTemplates.ua_dictionary(self.infinitive.word)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.INFINITIVE, self.infinitive.word]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_tense_tobe_note(self,  tobe_form: TobePastTemseForms) -> UEICNote:
        i: int = [self.past_tense.index(
            form) for form in self.past_tense if form.word == str(tobe_form)][0]
        tobe_prompt: Callable[[str, str, str], str]

        if tobe_form == TobePastTemseForms.WAS:
            tobe_prompt = TobePromptTemplates.past_tense_was
        if tobe_form == TobePastTemseForms.WERE:
            tobe_prompt = TobePromptTemplates.past_tense_were

        uuid: str = self.past_tense_uuid[i]
        prompt: str = tobe_prompt(
            self.infinitive.word, self.past_tense[i].word, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.word, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_tense[i].word, self.past_tense[i].reading),
            NoteTemplates.ua_dictionary(self.infinitive.word)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_TENSE, self.infinitive.word]

        return UEICNote.create(uuid, prompt, notes, tags)

    def __create_past_participle_tobe_note(self) -> UEICNote:
        uuid: str = self.past_participle_uuid
        prompt: str = TobePromptTemplates.past_participle(
            self.infinitive.word, self.past_participle.word, self.context)
        notes: list[str] = [
            NoteTemplates.infinitive_with_reading_and_translation(
                self.infinitive.word, self.infinitive.reading, self.translation),
            NoteTemplates.conjugation_with_reading(
                self.past_participle.word, self.past_participle.reading),
            NoteTemplates.ua_dictionary(self.infinitive.word)
        ]
        tags: list[str] = [self.verb_type,
                           AnkiNoteType.PAST_PARTICIPLE, self.infinitive.word]

        return UEICNote.create(uuid, prompt, notes, tags)
