# Index

1. [Classes](#classes)
2. [Enums](#enums)
3. [Templates](#templates)
4. [Special Files](#special-files)

# Classes

## [Verb](verb.py)

Represents a single verb in a English language. Includes infinitive, 3 sg present, past and past participle conjugation forms with thier reading; also has a context for templates and translation in Ukrainian.<br>

### Properties

`infinitive: Word` -  the infinitive form of a verb.<br>
`present_tense: Word | list[Word]` - the 3rd singlular present tense form of a verb; It is a list when a verb is the **to be**.<br>
`past_tense: Word | list[Word]` - the past tense form of a verb. It is a list when a verb is the **to be**.<br>
`past_participle: Word` - the past participle form of a verb.<br>
`regular_past_tense: Word | None` - the regular past tense form of a verb if there is one, otherwise it is `None`.<br>
`regular_past_participle: Word | None` - the regular past participle form of a verb if there is one, otherwise it is `None`.<br>
`context: str` - the posible context for the templates to show in the notes.<br>
`translation: str` - the translation to the Ukrainian language. You can change the translation in the [json file](static/Eng%20Irregular%20Verbs.json) to your respective language and then run the [sctipt](script.py) to create a deck of cards with translation to your language.<br>
`infinitive_uuid: str | list[str]` - the UUID for the **infinitive note** to secure the updatability of the note. It is a list when a verb is the **to be**.<br>
`past_tense_uuid: str | list[str]` - the UUID for the **past tense note** to secure the updatability of the note.It is a list when a verb is the **to be**.<br>
`past_participle_uuid: str` - the UUID for the **past participle note** to secure the updatability of the note.<br>
`anki_notes: list[UEICNote]` - the list of the anki notes made from the properties above.<br>
`is_tobe: bool` - it is `true` if a verb is the **to be**, otherwise it is `false`.<br>
`verb_type: VerbType` - the type of a verb.  For verbs like bet - bet - bet it is `VerbType.SAME_SAME_SAME`, for bend - bent - bent it is `VerbType.DIF_SAME_SAME` and for awake - awoke - awoken it is `VerbType.DIF_DIF_DIF`.<br>

### Methods

`__init__(self, verb: StoredVerb) -> None` - the constructor that takes a [StoredVerb](stored_verb.py) object and sets the properties with the data from a [StoredVerb](stored_verb.py) object.<br>

## [Word](verb.py)

The class created for storing word's spelling and reading.<br>

### Properties

`spelling: str` - the spelling of a word.<br>
`reading: str` - the reading of a word in IPA.<br>

### Methods

`__init__(self, spelling: str, reading: str) -> None` - the constructor that takes a spelling and a reading of a word and sets respective properties.<br>

## [StoredVerb](stored_verb.py)

`infinitive: str` - the infinitive form of a verb.<br>
`present_tense: str | list[str]` - the 3rd singular present tense form of a verb. It is a list when it is the **to be**.<br>
`past_tense: str | list[str]` - the past tense form of a verb. It is a list when it is the **to be** or has the regular past tense form.<br>
`past_participle: str | list[str]` - the past participle form of a verb. It is a list when it has the regular past participle form.<br>
`infinitive_reading: str` - the reading for infinitive.<br>
`present_tense_reading: str | list[str]` - the reading for 3rd singular present tense form. It is a list when it is the **to be**<br>
`past_tense_reading: str | list[str]` - the reading for past tense form. It is a list when it is the **to be** or has the regular past tense form.<br>
`past_participle_reading: str | list[str]` - the reading for past pasrticiple form. It is a list when it has the regular past participle form.<br>
`context: str` - the posible context for the templates to show in the notes.<br>
`translation: str | list[str]` - the translation to the Ukrainian language. It is a list when there are more than one translation. You can change the translation in the [json file](static/Eng%20Irregular%20Verbs.json) to your respective language and then run the [sctipt](script.py) to create a deck of cards with translation to your language.<br>
`infinitive_uuid: str | list[str]` - the UUID for the **infinitive note** to secure the updatability of the note. It is a list when a verb is the **to be**.<br>
`past_tense_uuid: str | list[str]` - the UUID for the **past tense note** to secure the updatability of the note.It is a list when a verb is the **to be**.<br>
`past_participle_uuid: str` - the UUID for the **past participle note** to secure the updatability of the note.<br>

### Methods

`__init__(self, values: dict) -> None` - the constructor that take a dictionary of values parsed from the [json file](static/Eng%20Irregular%20Verbs.json) and sets the properties.<br>

## [UEICNote](ueic_note.py)

The class used for creating anki notes.<br>

### Parents

`genanki.Note`

### Methods

`create(uuid: str, prompt: str, notes: list[str], tags: list[str], similar: list[str]) -> UEICNote` - the **static** method that creates an anki note.<br>
Arguments:
- `uuid: str` - the unique uuid.
- `prompt: str` - the prompt.
- `notes: list[str]` - a list of notes.
- `tags: list[str]` - a list of tags.
- `similar: list[str] | None` - a list of similar verbs with the same conjugation pattern. By default it is `None`.

Returns:
- `UEICNote` - the new anki note.

# Enums

## [AnkiNoteType](enums.py)

The list of anki note types.<br>

## [VerbType](enums.py)

The list of verb types.<br>

## [TobePresentTenseForms](enums.py)

The list of present tense forms of the verb **to be**.<br>

## [TobePastTemseForms](enums.py)

Thel ist of past tense forms of the verb **to be**.<br>

# Templates

I'm lazy to do it. The names of templates are self explaining.

# Special Files

## [script.py](script.py)

The main script of the project that creates the [Ultimate English Irregular Conjugation.apkg](Ultimate%20English%20Irregular%20Conjugation.apkg).<br>

## [commom.py](common.py)

The file with common things. like variables and methods.<br>

## [enums.py](enums.py)

The file with all enums of this project.<br>

## [front.html](static/front.html)

The front side of the card in a anki note. The script takes this data and put it inside a model of the note as the front side of the card.<br>

## [back.html](static/back.html)

The back side of the card in a amki note. The script takes this data and put it inside a model of the note as the back side of the card.<br>

## [style.css](static/style.css)

The styles for the cards. The script takes this data and put it inside a model of the note as the styles of the card for the front and back sides.<br>

## [template.html](static/template.html)

The templates for prompt, similar and notes fields in an anki note. The sript doesn't use this file to pars templates for notes. So you need to change it both in this file and in the template files.<br>