"""Streamlit page, Exercise 2 Task 4.

Run: streamlit run src/exercise_three/app_translator.py
"""

import streamlit as st

from exercise_three.exercise2_translator import (
    LANGUAGES,
    TEMPLATE_WITH_GLOSSARY,
    TONES,
    translate_campaign,
)

st.title("Marketing Campaign Translator")
key = st.sidebar.text_input("API Key", type="password")
text = st.text_area("Campaign copy", height=150)
lang = st.selectbox("Target language", LANGUAGES)
tone = st.selectbox("Tone", TONES)

if st.button("Translate"):
    if not key or not text:
        st.warning("Fill in the key and text first.")
    else:
        with st.spinner("Translating..."):
            st.write(
                translate_campaign(
                    text, lang, tone, template=TEMPLATE_WITH_GLOSSARY, api_key=key
                )
            )
