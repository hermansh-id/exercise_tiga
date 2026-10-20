"""Streamlit page, Exercise 3 Task 4.

Run: streamlit run src/exercise_three/app_pii.py
"""

import streamlit as st

from exercise_three.exercise3_pii import find_pii, highlight, regex_safety_net

st.title("PII Censor")
st.caption("Dummy data only: text is sent to OpenAI.")
key = st.sidebar.text_input("API Key", type="password")
text = st.text_area("Paste document here", height=200)

if st.button("Detect & Censor"):
    if not key or not text:
        st.warning("Fill in the key and text first.")
    else:
        with st.spinner("Detecting PII..."):
            ents = find_pii(text, api_key=key)
        censored = text
        for e in sorted(ents, key=lambda e: len(e["text"]), reverse=True):
            censored = censored.replace(e["text"], f"[{e['label']}]")
        censored = regex_safety_net(censored)

        st.subheader("Detected entities")
        st.markdown(highlight(text, ents).replace("\n", "<br>"), unsafe_allow_html=True)
        st.table(ents)
        st.subheader("Censored text")
        st.write(censored)
