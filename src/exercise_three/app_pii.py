"""Streamlit page, Exercise 3 Task 4.

Run: streamlit run src/exercise_three/app_pii.py
"""

import streamlit as st

from exercise_three.exercise3_pii import censor, find_pii

st.title("PII Censor")
key = st.sidebar.text_input("API Key", type="password")

# TODO: text_area input + tombol.
# Tampilkan: (1) teks dengan entity di-highlight (st.markdown, mis. :red[...]
# atau <mark>), (2) hasil censor(), (3) tabel entity dari find_pii().
