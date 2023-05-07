import json
from typing import Callable
from uuid import *

from genanki import *

from common import *
from models import *


def get_verbs() -> list[Verb]:
    with open("Eng Irregular Verbs.json", "r", encoding="utf8") as f:
         verbs: list[dict] = json.loads(f.read())["Sheet"]

    return [Verb(verb) for verb in verbs]


def create_uuid(infinitive: str, conjugation: str) -> UUID:
    return uuid5(NAMESPACE_DNS, infinitive+conjugation)


def create_note(uuid: UUID, prompt: str, notes: list[str], similar: list[str] | None = None) -> Note:
    uuid: str = str(uuid)
    similar: str = "" if similar == None else "".join(similar)
    notes: str = "".join(notes)

    return UEICNote(fields=[uuid, prompt, similar, notes])


def create_conjugation_note(
    infinitive: str, infinitive_reading: str,
    conjugation: str | list[str], conjugation_reading: str | list [str],
    context: str, translation: str | list[str],
    prompt: Callable[[str, str, str], str]
) -> Note:
    regular_conjugation: str | None = None
    regular_conjugation_reading: str | None = None
    
    if isinstance(conjugation, list):
        conjugation: str = conjugation[0]
        conjugation_reading: str = conjugation_reading[0]
        regular_conjugation: str = conjugation[1]
        regular_conjugation_reading: str = conjugation_reading[1]
    
    uuid: UUID = create_uuid(infinitive, conjugation)
    prompt: str = prompt(infinitive, conjugation, context)
    notes: list[str] = []

    notes.append(NoteTemplates.infinitive_with_reading_and_translation(
        infinitive, infinitive_reading, translation))
    notes.append(NoteTemplates.conjugation_with_reading(
        conjugation, conjugation_reading))
    if regular_conjugation != None:
        notes.append(NoteTemplates.regular_conjugation_with_reading(
            regular_conjugation, regular_conjugation_reading))
    notes.append(NoteTemplates.ua_dictionary(infinitive))

    return create_note(uuid, prompt, notes)


def create_infinitive_note(verb: Verb) -> Note:
    return create_conjugation_note(
        verb.infinitive, verb.infinitive_reading,
        verb.present_tense, verb.present_tense_reading,
        verb.context, verb.translation,
        PromptTemplates.infinitive
    )


def create_past_tense_note(verb: Verb) -> Note:
    return create_conjugation_note(
        verb.infinitive, verb.infinitive_reading,
        verb.past_tense, verb.past_tense_reading,
        verb.context, verb.translation,
        PromptTemplates.past_tense
    )


def create_past_participle_note(verb: Verb) -> Note:
    return create_conjugation_note(
        verb.infinitive, verb.infinitive_reading,
        verb.past_participle, verb.past_participle_reading,
        verb.context, verb.translation,
        PromptTemplates.past_participle
    )


def create_full_set_of_notes(verb: Verb) -> list[Note]:
    return [
        create_infinitive_note(verb),
        create_past_tense_note(verb),
        create_past_participle_note(verb)
    ]


def create_full_set_of_notes_for_tobe(verb: Verb) -> list[Note]:
    if verb.infinitive != "be":
        raise Exception()
    
    return [
        create_conjugation_note(
            verb.infinitive, verb.infinitive_reading,
            verb.present_tense[0], verb.present_tense_reading[0],
            verb.context, verb.translation,
            ToBePromptTemplates.infinitive_am
        ),
        create_conjugation_note(
            verb.infinitive, verb.infinitive_reading,
            verb.present_tense[1], verb.present_tense_reading[1],
            verb.context, verb.translation,
            ToBePromptTemplates.infinitive_is
        ),
        create_conjugation_note(
            verb.infinitive, verb.infinitive_reading,
            verb.present_tense[2], verb.present_tense_reading[2],
            verb.context, verb.translation,
            ToBePromptTemplates.infinitive_are
        ),
        create_conjugation_note(
            verb.infinitive, verb.infinitive_reading,
            verb.past_tense[0], verb.past_tense_reading[0],
            verb.context, verb.translation,
            ToBePromptTemplates.past_tense_was
        ),
        create_conjugation_note(
            verb.infinitive, verb.infinitive_reading,
            verb.past_tense[1], verb.past_tense_reading[1],
            verb.context, verb.translation,
            ToBePromptTemplates.past_tense_were
        ),
        create_conjugation_note(
            verb.infinitive, verb.infinitive_reading,
            verb.past_participle, verb.past_participle_reading,
            verb.context, verb.translation,
            ToBePromptTemplates.past_participle
        )
    ]


if __name__ == "__main__":
    verbs = get_verbs()
    
    for verb in verbs:
        if verb.infinitive == "be":
            [UEICDeck.add_note(note) for note in create_full_set_of_notes_for_tobe(verb)]
        else:
            [UEICDeck.add_note(note) for note in create_full_set_of_notes(verb)]
    
    Package(UEICDeck).write_to_file("Ultimate English Irregular Conjugation.apkg")        
    