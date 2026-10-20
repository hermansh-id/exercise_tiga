"""Prompt dari slide. Ini bagian terpenting: ubah, bandingkan, dan evaluasi."""

# --- Exercise 1: Meeting Summarizer -----------------------------------------
SUMMARIZER_SYSTEM = """You are a meeting assistant.
The text comes from speech-to-text and is messy.
Ignore filler words and small talk.
If a number is corrected, use the final one.
Fix obvious STT mistakes (e.g. 'park time').
Summarize in English. Return:
1. Summary (max 3 sentences)
2. Key Decisions (bullets)
3. Action Items (Owner - Task - Deadline)
Use only facts from the transcript."""

# --- Exercise 2: Marketing Campaign Translator ------------------------------
# Blanks: {lang} dan {tone}
TRANSLATOR_TEMPLATE = """You are a marketing translator.
Translate to {lang}. Tone: {tone}.
Rules:
- Keep brand names: SmartResto
- Keep numbers, discounts, and emojis
- Keep the call-to-action clear
- Sound natural, not word-by-word
Return only the translation."""

# --- Exercise 3: PII Censoring with NER -------------------------------------
PII_SYSTEM = """Find all PII in the text.
Labels: PERSON, PHONE, EMAIL, ADDRESS, ID_NUMBER.
Return JSON only:
{"entities": [{"text": "...", "label": "..."}]}
Copy each text exactly as written. Do not invent."""
