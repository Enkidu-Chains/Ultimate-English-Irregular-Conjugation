class NoteTemplates:
    @staticmethod
    def infinitive_with_reading_and_translation(infinitive: str, infinitive_reading: str, translation: str) -> str:
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
        