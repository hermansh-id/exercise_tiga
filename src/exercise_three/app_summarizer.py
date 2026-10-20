"""Streamlit page, Exercise 1 Task 5.

Run: streamlit run src/exercise_three/app_summarizer.py
"""

import streamlit as st

from exercise_three.llm import ask_llm
from exercise_three.prompts import SUMMARIZER_SYSTEM

st.title("Meeting Summarizer")
key = st.sidebar.text_input("API Key", type="password")
text = st.text_area("Paste transcript here", height=250)

# TODO: tombol 'Summarize'. Jika key atau text kosong -> st.warning(...).
# Jika terisi: st.spinner + st.write(ask_llm(SUMMARIZER_SYSTEM, text, api_key=key))
