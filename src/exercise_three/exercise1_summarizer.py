"""Exercise 1: Meeting Summarizer.

Run: python -m exercise_three.exercise1_summarizer
"""

from exercise_three.data import TRANSCRIPT
from exercise_three.llm import ask_llm
from exercise_three.prompts import SUMMARIZER_SYSTEM


def summarize(transcript: str, system: str = SUMMARIZER_SYSTEM) -> str:
    return ask_llm(system, transcript)


# TODO Task 2: tulis prompt versi Bahasa Indonesia.
# Salin SUMMARIZER_SYSTEM dari prompts.py lalu ubah bahasa outputnya.
SUMMARIZER_SYSTEM_ID = ""

# TODO Task 3: prompt TANPA 'messy-input rules'
# (filler words, final number, STT mistakes). Bandingkan hasilnya.
SUMMARIZER_SYSTEM_NO_RULES = ""

# TODO Task 4: tulis transcript berantakan sendiri (20+ baris):
# filler, koreksi angka, salah dengar, interupsi, perubahan keputusan.
MY_TRANSCRIPT = ""


if __name__ == "__main__":
    # Task 1: jalankan pada dummy transcript.
    print(summarize(TRANSCRIPT))

    # TODO Task 2-4: panggil summarize() dengan prompt/transcript milikmu,
    # lalu bandingkan outputnya dengan hasil Task 1.

    # TODO Evaluate (cek manual, QAEval-style):
    #   - 32% atau 30%?
    #   - 2 atau 3 kurir?
    #   - siapa mengerjakan apa, deadline kapan?
    #   - refund complaint sudah ditandai "dibahas rapat depan"?
