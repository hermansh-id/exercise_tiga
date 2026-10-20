"""Exercise 3: PII Censoring with NER.

Run: python -m exercise_three.exercise3_pii
"""

import json

from exercise_three.data import PII_DOC
from exercise_three.llm import ask_llm
from exercise_three.prompts import PII_SYSTEM


def find_pii(text, api_key=None):
    """Step 1: LLM menemukan entity, dikembalikan sebagai list of dict."""
    raw = ask_llm(PII_SYSTEM, text, json_mode=True, api_key=api_key)
    # Common error: JSONDecodeError -> bungkus json.loads() dengan try/except.
    return json.loads(raw)["entities"]


def censor(text, api_key=None):
    """Step 2: Python mengganti tiap entity dengan [LABEL]."""
    ents = find_pii(text, api_key)
    # Entity panjang dulu, supaya 'Budi Santoso' tidak terpotong oleh 'Budi'.
    ents.sort(key=lambda e: len(e["text"]), reverse=True)
    for e in ents:
        text = text.replace(e["text"], f"[{e['label']}]")
    return text


# TODO Task 1: 3 dokumen dengan PII berbeda (dummy saja!).
DOCS = []


# TODO Task 2: safety net regex untuk email & nomor telepon.
# Jalankan SETELAH censor(); tangkap PII yang lolos dari LLM.
def regex_safety_net(text: str) -> str:
    raise NotImplementedError


# TODO Task 3: hitung recall manual untuk tiap dokumen:
#   recall = PII ditemukan / total PII sebenarnya
# Tulis hasilnya di README.


if __name__ == "__main__":
    print(find_pii(PII_DOC))
    print(censor(PII_DOC))
    # TODO Task 1-3: jalankan pada DOCS, bandingkan dengan & tanpa regex.
