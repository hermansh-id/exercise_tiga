"""Streamlit page, Exercise 2 Task 4.

Run: streamlit run src/exercise_three/app_translator.py
"""

import streamlit as st

from exercise_three.exercise2_translator import translate_campaign

st.title("Marketing Campaign Translator")
key = st.sidebar.text_input("API Key", type="password")

# TODO: text_area untuk copy, selectbox bahasa, selectbox tone, tombol Translate.
# Catatan: translate_campaign() belum menerima api_key. Tambahkan parameter
# api_key ke translate_campaign() dan teruskan ke ask_llm().
