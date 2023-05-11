import json
import genanki

from stored_verb import StoredVerb

UEICDeck = genanki.Deck(
    1514828717,
    "Ultimate English Irregular Conjugation"
)


front_card = open("static/front.html", "r")
back_card = open("static/back.html", "r")
styles = open("static/style.css", "r")

UEICModel = genanki.Model(
    1311474809,
    "Ultimate English Irregular Conjugation",
    fields = [
        { "name": "UUID" },
        { "name": "Prompt" },
        { "name": "Similar" },
        { "name": "Notes" }
    ],
    templates = [
        {
            "name": "Card 1",
            "qfmt": front_card.read(),
            "afmt": back_card.read()
        }
    ],
    css = styles.read(),
    model_type = genanki.Model.CLOZE,
    sort_field_index = 1
)

front_card.close()
back_card.close()
styles.close()


def get_verbs() -> list[StoredVerb]:
    with open("static/Eng Irregular Verbs.json", "r", encoding="utf8") as f:
        verbs: list[dict] = json.loads(f.read())["Verbs"]

    return [StoredVerb(verb) for verb in verbs]
