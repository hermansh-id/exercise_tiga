"""Exercise 2: Marketing Campaign Translator.

Run: python -m exercise_three.exercise2_translator
"""

from exercise_three.data import CAMPAIGN_COPY
from exercise_three.llm import ask_llm
from exercise_three.prompts import TRANSLATOR_TEMPLATE


def translate_campaign(text, lang, tone="friendly", template=TRANSLATOR_TEMPLATE):
    system = template.format(lang=lang, tone=tone)
    return ask_llm(system, text)


# TODO Task 1: 3 teks promo berbeda, masing-masing ke 2 bahasa.
PROMO_TEXTS = []

# TODO Task 3: template baru dengan glossary rule,
# mis. "Always keep 'Paket Hemat' as is." (tetap pakai {lang} dan {tone}).
TEMPLATE_WITH_GLOSSARY = ""


if __name__ == "__main__":
    for lang in ["Indonesian", "Japanese"]:
        print(lang, "->", translate_campaign(CAMPAIGN_COPY, lang))

    # TODO Task 2: bandingkan tone='friendly' vs tone='formal'.
    # TODO Task 1 & 3: loop PROMO_TEXTS x bahasa, lalu coba glossary rule.

    # Evaluate: BLEU butuh terjemahan referensi; untuk iklan,
    # cek manual nada (tone) lebih penting. Catat penilaianmu di README.
