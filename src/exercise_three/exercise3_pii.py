"""Exercise 3: PII Censoring with NER.

Run: python -m exercise_three.exercise3_pii
"""

import html
import json
import re

from exercise_three.data import PII_DOC
from exercise_three.llm import ask_llm
from exercise_three.prompts import PII_SYSTEM


def find_pii(text, api_key=None):
    """Step 1: LLM menemukan entity, dikembalikan sebagai list of dict."""
    raw = ask_llm(PII_SYSTEM, text, json_mode=True, api_key=api_key)
    try:
        return json.loads(raw)["entities"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def censor(text, api_key=None):
    """Step 2: Python mengganti tiap entity dengan [LABEL]."""
    ents = find_pii(text, api_key)
    # Entity panjang dulu, supaya 'Budi Santoso' tidak terpotong oleh 'Budi'.
    ents.sort(key=lambda e: len(e["text"]), reverse=True)
    for e in ents:
        text = text.replace(e["text"], f"[{e['label']}]")
    return text


# Task 1: 3 dokumen dummy. 'pii' = ground truth buatan manusia (untuk recall).
DOCS = [
    {
        "text": PII_DOC,
        "pii": ["Budi Santoso", "budi@mail.com", "0812-3456-7890", "Sleman"],
    },
    {
        "text": (
            "Ibu Siti Rahmawati (siti.r@example.org, +62 813 5555 1212) "
            "tinggal di Jl. Kaliurang Km 5, Yogyakarta. NIK 3404123456789001."
        ),
        "pii": [
            "Siti Rahmawati",
            "siti.r@example.org",
            "+62 813 5555 1212",
            "Jl. Kaliurang Km 5, Yogyakarta",
            "3404123456789001",
        ],
    },
    {
        "text": (
            "Please ship to John Carter, 42 Maple Street, Springfield. "
            "Call 0857-1111-2222 or write to jcarter@corp.example. "
            "Passport X1234567."
        ),
        "pii": [
            "John Carter",
            "42 Maple Street, Springfield",
            "0857-1111-2222",
            "jcarter@corp.example",
            "X1234567",
        ],
    },
]

# Task 2: safety net regex untuk email & telepon (jalankan SETELAH censor()).
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE_RE = re.compile(r"(?:\+62|62|0)[\s-]?8\d{1,3}[\s-]?\d{3,4}[\s-]?\d{3,4}")


def regex_safety_net(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL]", text)
    return PHONE_RE.sub("[PHONE]", text)


def censor_safe(text, api_key=None):
    """LLM censor + regex safety net."""
    return regex_safety_net(censor(text, api_key))


# Task 3: recall = PII ditemukan / total PII sebenarnya.
# 'Ditemukan' = string PII sudah tidak muncul di teks hasil sensor.
def recall(censored: str, truth: list[str]) -> float:
    if not truth:
        return 1.0
    return sum(1 for t in truth if t not in censored) / len(truth)


def leaked(censored: str, truth: list[str]) -> list[str]:
    return [t for t in truth if t in censored]


# Task 4 (dipakai Streamlit): highlight entity sebagai HTML <mark>.
def highlight(text: str, ents: list[dict]) -> str:
    texts = sorted({e["text"] for e in ents if e.get("text")}, key=len, reverse=True)
    labels = {e["text"]: e["label"] for e in ents if e.get("text")}
    escaped = html.escape(text)
    if not texts:
        return escaped
    pattern = re.compile("|".join(re.escape(html.escape(t)) for t in texts))
    by_escaped = {html.escape(t): labels[t] for t in texts}

    def mark(m):
        return f"<mark>{m.group(0)} <sub>{by_escaped[m.group(0)]}</sub></mark>"

    return pattern.sub(mark, escaped)


if __name__ == "__main__":
    print(find_pii(PII_DOC))
    print(censor(PII_DOC))

    print("\n=== Task 1-3: 3 dokumen, tanpa vs dengan regex ===")
    for i, doc in enumerate(DOCS, 1):
        llm_only = censor(doc["text"])
        with_regex = regex_safety_net(llm_only)
        print(f"\nDoc {i}: {llm_only}")
        print(f"  recall LLM saja   : {recall(llm_only, doc['pii']):.0%} bocor={leaked(llm_only, doc['pii'])}")
        print(f"  recall LLM + regex: {recall(with_regex, doc['pii']):.0%} bocor={leaked(with_regex, doc['pii'])}")
