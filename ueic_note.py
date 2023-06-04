import genanki

from common import UEICModel


class UEICNote(genanki.Note):
    @staticmethod
    def create(uuid: str, prompt: str, notes: list[str], tags: list[str],
               similar: list[str] | None = None) -> "UEICNote":
        similar: str = "" if similar == None else "".join(similar)
        notes: str = "".join(notes)

        return UEICNote(model=UEICModel, fields=[uuid, prompt, similar, notes], tags=tags, guid=uuid)
