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
