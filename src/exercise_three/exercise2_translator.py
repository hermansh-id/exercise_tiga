"""Exercise 2: Marketing Campaign Translator.

Run: python -m exercise_three.exercise2_translator
"""

from exercise_three.data import CAMPAIGN_COPY
from exercise_three.llm import ask_llm
from exercise_three.prompts import TRANSLATOR_TEMPLATE


def translate_campaign(
    text, lang, tone="friendly", template=TRANSLATOR_TEMPLATE, api_key=None
):
    system = template.format(lang=lang, tone=tone)
    return ask_llm(system, text, api_key=api_key)


# Task 1: 3 teks promo berbeda.
PROMO_TEXTS = [
    CAMPAIGN_COPY,
    "Buy 1 Get 1 Free every Friday! Grab your favorite coffee at SmartResto ☕",
    "Free delivery for orders above $10. Hungry? SmartResto is one tap away!",
]

# Task 3: glossary rule. Tetap pakai {lang} dan {tone}.
TEMPLATE_WITH_GLOSSARY = """You are a marketing translator.
Translate to {lang}. Tone: {tone}.
Rules:
- Keep brand names: SmartResto
- Glossary: always keep 'Paket Hemat' exactly as is, never translate it
- Keep numbers, discounts, and emojis
- Keep the call-to-action clear
- Sound natural, not word-by-word
Return only the translation."""

GLOSSARY_TEXT = "Try our Paket Hemat: 2 meals + 1 drink for only $5. Order at SmartResto!"

LANGUAGES = ["Indonesian", "Japanese"]
TONES = ["friendly", "formal"]


if __name__ == "__main__":
    print("=== Expected demo ===")
    for lang in LANGUAGES:
        print(lang, "->", translate_campaign(CAMPAIGN_COPY, lang))

    print("\n=== Task 1: 3 promo x 2 bahasa ===")
    for text in PROMO_TEXTS:
        print("\nEN:", text)
        for lang in LANGUAGES:
            print(" ", lang, "->", translate_campaign(text, lang))

    print("\n=== Task 2: friendly vs formal ===")
    for tone in TONES:
        print(f"[{tone}] Indonesian ->", translate_campaign(CAMPAIGN_COPY, "Indonesian", tone))

    print("\n=== Task 3: glossary ===")
    for label, template in [("tanpa", TRANSLATOR_TEMPLATE), ("dengan", TEMPLATE_WITH_GLOSSARY)]:
        out = translate_campaign(GLOSSARY_TEXT, "Indonesian", template=template)
        kept = "Paket Hemat" in out
        print(f"[{label} glossary] kept={kept} -> {out}")

    # Evaluate: BLEU butuh terjemahan referensi; untuk iklan, cek nada
    # (tone) manual lebih penting. Catat penilaianmu di README.
