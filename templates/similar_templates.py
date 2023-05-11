class SimilarTemplates:
    @staticmethod
    def similar(infinitive: str, conjugation: str) -> str:
        return f"""
        <br>
        <span class="alt_conj">{conjugation}</span> ← <span class="alt_inf">{infinitive}</span>
        """
  