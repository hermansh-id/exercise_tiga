# Exercise 18: Building Simple LLM Apps

Tiga app LLM kecil dengan satu helper `ask_llm()`:
Meeting Summarizer, Marketing Campaign Translator, PII Censor (NER).

Scaffold sudah menyiapkan helper, prompt dari slide, dan data dummy.
Fokus kamu: **prompt, task di tiap exercise, dan evaluasi output**.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e . # atau: poetry install
cp .env.example .env # isi OPENAI_API_KEY
```

`.env` sudah ada di `.gitignore`. Jangan commit API key.
Ganti model lewat `OPENAI_MODEL`, bukan di kode.

## Struktur

| File | Isi | Status |
|---|---|---|
| `src/exercise_three/llm.py` | client + `ask_llm()` | siap pakai |
| `src/exercise_three/prompts.py` | prompt dari slide | siap, ubah untuk eksperimen |
| `src/exercise_three/data.py` | transcript, copy, dokumen PII dummy | siap |
| `exercise1_summarizer.py` | `summarize()` + TODO Task 2-4 | kerjakan |
| `exercise2_translator.py` | `translate_campaign()` + TODO Task 1-3 | kerjakan |
| `exercise3_pii.py` | `find_pii()`, `censor()` + TODO Task 1-3 | kerjakan |
| `app_summarizer.py`, `app_translator.py`, `app_pii.py` | Streamlit stub | kerjakan |

## Cara jalan

```bash
python -m exercise_three.exercise1_summarizer
python -m exercise_three.exercise2_translator
python -m exercise_three.exercise3_pii
streamlit run src/exercise_three/app_summarizer.py
```

## Exercise 1: Meeting Summarizer

Transcript STT sengaja berantakan: filler (`eee`, `anu`), koreksi angka
(30 -> 32 persen), salah dengar (`park time` = part time, `ri fan` = refund),
interupsi, dan perubahan keputusan (3 kurir jadi 2, Jumat dimundurkan).

- [ ] Task 1: jalankan summarizer pada dummy transcript
- [ ] Task 2: prompt output Bahasa Indonesia
- [ ] Task 3: hapus "messy-input rules", bandingkan hasil
- [ ] Task 4: tulis transcript berantakan sendiri (20+ baris), ringkas
- [ ] Task 5: Streamlit (text area, button, result)
- [ ] Evaluate: 32% atau 30%? 2 atau 3 kurir? Siapa mengerjakan apa?

Expected (acuan, bukan harus persis): ringkasan order online naik 32%, telat
8% jadi 15%, 2 kurir part-time dicoba 2 minggu, layar antrean tablet dapur;
Sari rekrut kurir (Jumat depan), Budi cek antrean (Senin depan), Dimas bikin
layar antrean (~2 minggu); rapat berikutnya Kamis depan 10:00.

## Exercise 2: Campaign Translator

Aturan: jaga brand name (`SmartResto`), angka/diskon/emoji, dan CTA; terdengar natural.

- [ ] Task 1: 3 teks promo ke 2 bahasa
- [ ] Task 2: bandingkan `tone='friendly'` vs `'formal'`
- [ ] Task 3: tambah glossary rule (mis. selalu pertahankan `Paket Hemat`)
- [ ] Task 4: Streamlit (teks, pilih bahasa, pilih tone)
- [ ] Evaluate: BLEU butuh referensi; untuk iklan, cek nada manual lebih penting

## Exercise 3: PII Censoring with NER

Dua langkah: LLM menemukan entity (JSON) lalu Python mengganti dengan `[LABEL]`.
Label: PERSON, PHONE, EMAIL, ADDRESS, ID_NUMBER.

> Teks dikirim ke OpenAI. Pakai **data dummy saja**.
> Production: deteksi PII lokal dulu (regex / NER on-premise) sebelum cloud LLM.

- [ ] Task 1: `censor()` pada 3 dokumen dengan PII berbeda
- [ ] Task 2: regex safety net untuk email & telepon
- [ ] Task 3: hitung recall manual = PII ditemukan / total PII sebenarnya
- [ ] Task 4: Streamlit yang highlight entity

## Common errors

| Error | Solusi |
|---|---|
| `AuthenticationError (401)` | API key kosong/salah, cek `.env` |
| `model_not_found (404)` | akun tak bisa pakai model itu; `client.models.list()` |
| `BadRequestError (400)` | parameter tak didukung model; hapus parameternya |
| `RateLimitError (429)` | terlalu banyak request / kredit habis; tunggu, cek billing |
| `JSONDecodeError` | pakai `json_mode=True`, bungkus `json.loads()` dengan try/except |

## Catatan hasil (isi sendiri)

- Ex 1: apa beda output dengan/tanpa messy-input rules?
- Ex 2: beda friendly vs formal?
- Ex 3: recall per dokumen, apa yang lolos? Ada PII halusinasi?
