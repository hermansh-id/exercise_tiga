"""Offline tests: OpenAI di-mock, tidak butuh API key."""

import json

import pytest

from exercise_three import exercise1_summarizer, exercise2_translator, exercise3_pii, llm
from exercise_three.data import PII_DOC, TRANSCRIPT


class FakeClient:
    def __init__(self, reply):
        self.calls = []
        self.reply = reply
        self.chat = self
        self.completions = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        msg = type("M", (), {"content": self.reply})
        return type("R", (), {"choices": [type("C", (), {"message": msg})]})


@pytest.fixture
def fake(monkeypatch):
    def install(reply):
        client = FakeClient(reply)
        monkeypatch.setattr(llm, "get_client", lambda api_key=None: client)
        return client

    return install


def test_ask_llm_messages_and_json_mode(fake):
    c = fake("hi")
    assert llm.ask_llm("sys", "usr") == "hi"
    assert c.calls[0]["messages"] == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ]
    assert "response_format" not in c.calls[0]
    llm.ask_llm("sys", "usr", json_mode=True)
    assert c.calls[1]["response_format"] == {"type": "json_object"}


def test_summarize_sends_transcript(fake):
    c = fake("summary")
    assert exercise1_summarizer.summarize(TRANSCRIPT) == "summary"
    assert c.calls[0]["messages"][1]["content"] == TRANSCRIPT
    assert "meeting assistant" in c.calls[0]["messages"][0]["content"]


def test_translate_fills_template(fake):
    c = fake("x")
    exercise2_translator.translate_campaign("copy", "Japanese", tone="formal")
    system = c.calls[0]["messages"][0]["content"]
    assert "Translate to Japanese. Tone: formal." in system
    assert "{" not in system


def test_censor_replaces_longest_first(fake):
    ents = [
        {"text": "Budi", "label": "PERSON"},
        {"text": "Budi Santoso", "label": "PERSON"},
        {"text": "budi@mail.com", "label": "EMAIL"},
        {"text": "0812-3456-7890", "label": "PHONE"},
        {"text": "Sleman", "label": "ADDRESS"},
    ]
    fake(json.dumps({"entities": ents}))
    out = exercise3_pii.censor(PII_DOC)
    assert "[PERSON]" in out and "Santoso" not in out
    assert "budi@mail.com" not in out and "0812" not in out and "Sleman" not in out
    assert "#4521" in out


def test_data_transcript_shape():
    lines = TRANSCRIPT.strip().splitlines()
    assert len(lines) == 28
    assert "[inaudible]" in TRANSCRIPT


def test_regex_safety_net_catches_leaks():
    out = exercise3_pii.regex_safety_net(
        "mail a.b+c@x.co.id call 0812-3456-7890 or +62 813 5555 1212 order #4521"
    )
    assert out == "mail [EMAIL] call [PHONE] or [PHONE] order #4521"


def test_regex_covers_all_dummy_docs():
    for doc in exercise3_pii.DOCS:
        out = exercise3_pii.regex_safety_net(doc["text"])
        for t in doc["pii"]:
            if "@" in t:
                assert t not in out
    # Telepon Indonesia tertangkap; dokumen 3 (0857-...) juga.
    assert "0812-3456-7890" not in exercise3_pii.regex_safety_net(exercise3_pii.DOCS[0]["text"])
    assert "+62 813 5555 1212" not in exercise3_pii.regex_safety_net(exercise3_pii.DOCS[1]["text"])
    assert "0857-1111-2222" not in exercise3_pii.regex_safety_net(exercise3_pii.DOCS[2]["text"])


def test_recall_and_leaked():
    truth = ["Budi", "a@b.co", "Sleman"]
    assert exercise3_pii.recall("[PERSON] a@b.co [ADDRESS]", truth) == pytest.approx(2 / 3)
    assert exercise3_pii.leaked("[PERSON] a@b.co [ADDRESS]", truth) == ["a@b.co"]


def test_censor_survives_bad_json(fake):
    fake("not json")
    assert exercise3_pii.censor("hello") == "hello"


def test_highlight_escapes_and_marks():
    out = exercise3_pii.highlight(
        "<b>Budi Santoso</b> & Budi", [{"text": "Budi Santoso", "label": "PERSON"}, {"text": "Budi", "label": "PERSON"}]
    )
    assert "&lt;b&gt;" in out and "<b>" not in out
    assert out.count("<mark>") == 2


def test_evaluate_flags_wrong_number():
    from exercise_three.exercise1_summarizer import evaluate

    good = "Orders rose 32%. 2 couriers. Sari will recruit. Dimas builds screen. Budi checks."
    bad = "Orders rose 30%."
    assert all(evaluate(good).values())
    assert not evaluate(bad)["32% atau 30%?"]


def test_summarizer_prompt_variants_differ():
    from exercise_three.exercise1_summarizer import (
        MY_TRANSCRIPT,
        SUMMARIZER_SYSTEM_ID,
        SUMMARIZER_SYSTEM_NO_RULES,
    )

    assert "Bahasa Indonesia" in SUMMARIZER_SYSTEM_ID
    assert "filler" not in SUMMARIZER_SYSTEM_NO_RULES
    assert len(MY_TRANSCRIPT.strip().splitlines()) >= 20


def test_glossary_template_formats():
    t = exercise2_translator.TEMPLATE_WITH_GLOSSARY.format(lang="Indonesian", tone="formal")
    assert "Paket Hemat" in t and "{" not in t
    assert len(exercise2_translator.PROMO_TEXTS) == 3
