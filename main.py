from genanki import *

from common import UEICDeck, get_verbs
from stored_verb import StoredVerb
from verb import Verb

if __name__ == "__main__":
    stored_verbs: list[StoredVerb] = get_verbs()
    verbs: list[Verb] = [Verb(stored_verb) for stored_verb in stored_verbs]

    [UEICDeck.add_note(anki_note) for verb in verbs for anki_note in verb.anki_notes]

    Package(UEICDeck).write_to_file(
        "[Shared] Ultimate English Irregular Conjugation.apkg")
