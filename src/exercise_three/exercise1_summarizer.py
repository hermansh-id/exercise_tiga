"""Exercise 1: Meeting Summarizer.

Run: python -m exercise_three.exercise1_summarizer
"""

from exercise_three.data import TRANSCRIPT
from exercise_three.llm import ask_llm
from exercise_three.prompts import SUMMARIZER_SYSTEM


def summarize(transcript: str, system: str = SUMMARIZER_SYSTEM, api_key=None) -> str:
    return ask_llm(system, transcript, api_key=api_key)


# Task 2: output Bahasa Indonesia.
SUMMARIZER_SYSTEM_ID = """You are a meeting assistant.
The text comes from speech-to-text and is messy.
Ignore filler words and small talk.
If a number is corrected, use the final one.
Fix obvious STT mistakes (e.g. 'park time').
Summarize in Bahasa Indonesia. Return:
1. Ringkasan (maks 3 kalimat)
2. Keputusan Utama (bullets)
3. Action Items (Penanggung jawab - Tugas - Tenggat)
Use only facts from the transcript."""

# Task 3: tanpa messy-input rules (filler, koreksi angka, salah dengar).
SUMMARIZER_SYSTEM_NO_RULES = """You are a meeting assistant.
Summarize in English. Return:
1. Summary (max 3 sentences)
2. Key Decisions (bullets)
3. Action Items (Owner - Task - Deadline)"""

# Task 4: transcript berantakan buatan sendiri (24 baris).
# Jebakan: filler, koreksi angka (5 jadi 7 hari), salah dengar
# ('stok epname' = stock opname, 'lon ching' = launching),
# interupsi, small talk, dan keputusan berubah (Rabu jadi Kamis).
MY_TRANSCRIPT = """
[00:00:03] Ayu: halo halo kedengeran ga ya eee kita mulai aja deh
[00:00:08] Raka: kedengeran mbak tapi agak pecah dikit hehe
[00:00:14] Ayu: oke topik kita hari ini lon ching fitur voucher sama stok gudang
[00:00:27] Raka: jadi gini mbak vouchernya rencana saya aktif lima hari
[00:00:34] Raka: eh bukan salah tujuh hari biar weekend kebawa
[00:00:45] Ayu: oke tujuh hari ya diskonnya berapa persen
[00:00:52] Tono: anu saya usul dua puluh persen aja mbak
[00:01:01] Ayu: hmm kebanyakan ga sih lima belas aja deh
[00:01:09] Tono: oke lima belas siap
[00:01:15] Raka: terus lon chingnya rabu ya mbak
[00:01:23] Ayu: eh btw ada yang bawa charger ga laptop saya mau mati
[00:01:30] Tono: ada mbak nanti saya pinjemin
[00:01:38] Ayu: makasih ya to lanjut tadi lon chingnya rabu
[00:01:44] Raka: bentar mbak tim desain baru siap kamis banner nya
[00:01:52] Ayu: yaudah kamis aja kalo gitu
[00:02:03] Tono: [inaudible] stok epname gudang kapan
[00:02:10] Ayu: nah iya stok epname minggu depan ya to kamu yang pegang
[00:02:18] Tono: siap mbak selasa depan saya mulai
[00:02:26] Raka: eee saya bikin banner brief dulu ke desain besok
[00:02:34] Ayu: oke raka besok ya terus tono hasil epname kirim ke saya jumat depan
[00:02:45] Tono: anu mbak sinyal putus putus
[00:02:51] Ayu: halo ok intinya voucher lima belas persen tujuh hari lon ching kamis
[00:03:02] Ayu: rapat lanjutan senin jam dua makasih semua
[00:03:06] Raka: sip makasih mbak
"""

# Evaluate: cek manual ala QAEval, dibuat otomatis (heuristik string).
# Tiap item: (pertanyaan, fungsi cek pada ringkasan lowercase).
QA_CHECKS = [
    ("32% atau 30%?", lambda s: "32" in s and "30%" not in s and "30 %" not in s),
    ("2 atau 3 kurir?", lambda s: "2" in s or "two" in s or "dua" in s),
    ("Sari merekrut kurir?", lambda s: "sari" in s and ("recruit" in s or "rekrut" in s)),
    ("Dimas bikin layar antrean?", lambda s: "dimas" in s),
    ("Budi cek antrean dapur?", lambda s: "budi" in s),
    ("AC / small talk tidak masuk?", lambda s: " ac " not in f" {s} " and "dingin" not in s),
]


def evaluate(summary: str, checks=QA_CHECKS) -> dict[str, bool]:
    s = summary.lower()
    return {q: bool(check(s)) for q, check in checks}


if __name__ == "__main__":
    # Task 1
    baseline = summarize(TRANSCRIPT)
    print("=== Task 1: baseline ===\n", baseline)

    # Task 2
    print("\n=== Task 2: Bahasa Indonesia ===\n", summarize(TRANSCRIPT, SUMMARIZER_SYSTEM_ID))

    # Task 3
    no_rules = summarize(TRANSCRIPT, SUMMARIZER_SYSTEM_NO_RULES)
    print("\n=== Task 3: tanpa messy-input rules ===\n", no_rules)

    # Task 4
    print("\n=== Task 4: transcript sendiri ===\n", summarize(MY_TRANSCRIPT))

    # Evaluate: bandingkan dengan vs tanpa rules.
    for name, out in [("dengan rules", baseline), ("tanpa rules", no_rules)]:
        print(f"\n=== Evaluate ({name}) ===")
        for q, ok in evaluate(out).items():
            print(("PASS" if ok else "FAIL"), q)
