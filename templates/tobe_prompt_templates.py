class TobePromptTemplates:
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
