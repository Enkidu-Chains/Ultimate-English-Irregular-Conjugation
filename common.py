import genanki

UEICDeck = genanki.Deck(
    1514828717,
    "Ultimate English Irregular Conjugation"
)


front_card = open("front.html", "r")
back_card = open("back.html", "r")
styles = open("style.css", "r")

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


class PromptTemplates:
    @staticmethod
    def infinitive(infinitive: str, present_tense: str, context: str) -> str:
        return f"""
        <span class="infinitive">⊙ The verb in ⊙</span><br>
        <span class="cloze_hilite">he/she {present_tense}</span> <span class="orientation_hint">({context})</span><br>
        is <span class="info_cloze">{{{{c1::{infinitive}}}}}</span>
        """
    
    @staticmethod
    def past_tense(infinitive: str, past_tense: str, context: str) -> str:
        return f"""
        <span class="past_tense">← At that time, ←</span><br>
        <br>
        <span class="cloze_pronoun">you</span> <span class="en_verb">{{{{c1::{past_tense}::...{infinitive}...}}}}</span> <span class="en_hint">({context})</span>
        """
    
    @staticmethod
    def past_participle(infinitive: str, past_participle: str, context: str) -> str:
        return f"""
        <span class="past_participle">Jonatan has</span> <span class="info_cloze">{{{{c1::{past_participle}::...{infinitive}...}}}}</span> <span class="orientation_hint">({context})</span>
        """


class SimilarTemplates:
    @staticmethod
    def similar(infinitive: str, conjugation: str) -> str:
        return f"""
        <br>
        <span class="alt_conj">{conjugation}</span> ← <span class="alt_inf">{infinitive}</span>
        """
    
    
class NoteTemplates:
    @staticmethod
    def infinitive_with_reading_and_translation(infinitive: str, infinitive_reading: str, translation: str | list[str]) -> str:
        if isinstance(translation, list):
            translation: str = ", ".join(translation)

        return f"""
        <br>
        <span class="camb"><a href="https://dictionary.cambridge.org/dictionary/english/{infinitive}">{infinitive}</a></span> is read <span class="note_highlight">[{infinitive_reading}]</span> and translated as: <span class="note_non_en_word">{translation}</span>
        """

    @staticmethod
    def conjugation_with_reading(conjugation: str, conjugation_reading: str) -> str:
        return f"""
        <br>
        conjugated form <span class="notes_en_form">{conjugation}</span> is read <span class="note_highlight">[{conjugation_reading}]</span>
        """
    
    @staticmethod
    def regular_conjugation_with_reading(regular_conjugation: str, regular_conjugation_reading: str) -> str:
        return f"""
        <br>
        regular conjugation <span class="notes_en_form">{regular_conjugation}</span> is also possible, it's read <span class="note_highlight">[{regular_conjugation_reading}]</span>
        """
    
    @staticmethod
    def ua_dictionary(infinitive: str) -> str:
        return f"""
        <br>
        <span class="camb"><a href="https://dictionary.cambridge.org/dictionary/english-ukrainian/{infinitive}">(UA dictionary)</a></span>
        """
        

class ToBePromptTemplates:
    @staticmethod
    def infinitive_am(infinitive: str, present_tense: str, context: str) -> str:
        return f"""
        <span class="infinitive">⊙ The verb in ⊙</span><br>
        <span class="cloze_hilite">I {present_tense}</span> <span class="orientation_hint">({context})</span><br>
        is <span class="info_cloze">{{{{c1::{infinitive}}}}}</span>
        """

    @staticmethod
    def infinitive_is(infinitive: str, present_tense: str, context: str) -> str:
        return f"""
        <span class="infinitive">⊙ The verb in ⊙</span><br>
        <span class="cloze_hilite">he/she {present_tense}</span> <span class="orientation_hint">({context})</span><br>
        is <span class="info_cloze">{{{{c1::{infinitive}}}}}</span>
        """

    @staticmethod
    def infinitive_are(infinitive: str, present_tense: str, context: str) -> str:
        return f"""
        <span class="infinitive">⊙ The verb in ⊙</span><br>
        <span class="cloze_hilite">you {present_tense}</span> <span class="orientation_hint">({context})</span><br>
        is <span class="info_cloze">{{{{c1::{infinitive}}}}}</span>
        """

    @staticmethod
    def past_tense_was(infinitive: str, past_tense: str, context: str) -> str:
        return f"""
        <span class="past_tense">← At that time, ←</span><br>
        <br>
        <span class="cloze_pronoun">he/she</span> <span class="en_verb">{{{{c1::{past_tense}::...{infinitive}...}}}}</span> <span class="en_hint">({context})</span>
        """

    @staticmethod
    def past_tense_were(
        infinitive: str, past_tense: str, context: str
    ) -> str:
        return f"""
        <span class="past_tense">← At that time, ←</span><br>
        <br>
        <span class="cloze_pronoun">you</span> <span class="en_verb">{{{{c1::{past_tense}::...{infinitive}...}}}}</span> <span class="en_hint">({context})</span>
        """

    @staticmethod
    def past_participle(infinitive: str, past_participle: str, context: str) -> str:
        return f"""
        <span class="past_participle">Jonatan has</span> <span class="info_cloze">{{{{c1::{past_participle}::...{infinitive}...}}}}</span> <span class="orientation_hint">({context})</span>
        """
    
