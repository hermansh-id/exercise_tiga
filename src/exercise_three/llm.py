"""Setup: OpenAI client + reusable ask_llm() helper (slides: Setup).

Dipakai oleh ketiga exercise. Tidak perlu diubah kecuali kamu mau eksperimen.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL")


def get_client(api_key: str | None = None) -> OpenAI:
    """Pakai api_key dari argumen (mis. input Streamlit), fallback ke .env."""
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def ask_llm(system, user, json_mode=False, api_key=None):
    """Kirim system + user prompt, kembalikan teks jawaban model.

    system:    aturan - siapa model dan bagaimana harus menjawab.
    user:      teks yang diproses.
    json_mode: paksa output JSON valid (berguna untuk NER).
    api_key:   opsional, override OPENAI_API_KEY dari .env.
    """
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    res = get_client(api_key).chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **kwargs,
    )
    return res.choices[0].message.content
