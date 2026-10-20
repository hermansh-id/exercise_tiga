"""Streamlit page, Exercise 1 Task 5.

Run: streamlit run src/exercise_three/app_summarizer.py
"""

import streamlit as st

from exercise_three.exercise1_summarizer import SUMMARIZER_SYSTEM_ID, summarize
from exercise_three.prompts import SUMMARIZER_SYSTEM

st.title("Meeting Summarizer")
key = st.sidebar.text_input("API Key", type="password")
lang = st.sidebar.radio("Output language", ["English", "Bahasa Indonesia"])
text = st.text_area("Paste transcript here", height=250)

if st.button("Summarize"):
    if not key or not text:
        st.warning("Fill in the key and text first.")
    else:
        system = SUMMARIZER_SYSTEM if lang == "English" else SUMMARIZER_SYSTEM_ID
        with st.spinner("Summarizing..."):
            st.write(summarize(text, system, api_key=key))
