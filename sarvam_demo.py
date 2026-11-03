"""
sarvam_demo.py
--------------
Simulated Sales Agent demo using Sarvam AI APIs.

Demonstrates:
  1. Chat completion  — sarvam-105b-conversations  →  AI lead qualification reply
  2. Translation      — Sarvam Translate (Mayura)  →  Hindi & Tamil versions
  3. Text-to-speech   — Bulbul v4-flash            →  saves reply.mp3

Run:
    python sarvam_demo.py

Requires SARVAM_API_KEY in .env
"""

import os
import base64
from dotenv import load_dotenv
from sarvamai import SarvamAI

# ── Load key from .env ──────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    raise EnvironmentError(
        "SARVAM_API_KEY not set. Add it to your .env file."
    )

client = SarvamAI(api_subscription_key=api_key)

print("=" * 60)
print("  Sales Agent — Sarvam AI Integration Demo")
print("=" * 60)

# ──────────────────────────────────────────────────────────────────────────────
# STEP 1 · Chat Completion
# Simulate an AI sales agent qualifying a lead
# ──────────────────────────────────────────────────────────────────────────────
print("\n[1/3] Chat Completion — Lead qualification\n")

system_prompt = (
    "You are Sales Agent, an AI outbound sales assistant. "
    "Your job is to qualify inbound leads politely and concisely. "
    "Keep replies under 3 sentences."
)

user_message = (
    "Hi, I saw your product online. We're a team of 40 "
    "and we're struggling to follow up with all our leads."
)

response = client.chat.completions(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_message},
    ],
    model="sarvam-105b-conversations",
)

agent_reply = response.choices[0].message.content
print(f"  Customer : {user_message}")
print(f"  Agent    : {agent_reply}")

# ──────────────────────────────────────────────────────────────────────────────
# STEP 2 · Translation  (Sarvam Translate — Mayura)
# Translate the agent reply into Hindi and Tamil
# ──────────────────────────────────────────────────────────────────────────────
print("\n[2/3] Translation — Multilingual outreach\n")

for lang_name, lang_code in [("Hindi", "hi-IN"), ("Tamil", "ta-IN")]:
    result = client.text.translate(
        input=agent_reply,
        source_language_code="en-IN",
        target_language_code=lang_code,
        model="mayura:v1",
    )
    # encode safely for terminals that don't support full Unicode
    safe = result.translated_text.encode("utf-8", errors="replace").decode("utf-8")
    print(f"  {lang_name}: {safe}".encode(
        "ascii", errors="backslashreplace").decode("ascii"))

# ──────────────────────────────────────────────────────────────────────────────
# STEP 3 · Text-to-Speech  (Bulbul v4-flash)
# Convert the English agent reply to audio and save as reply.mp3
# ──────────────────────────────────────────────────────────────────────────────
print("\n[3/3] Text-to-Speech — Voice reply (Bulbul v4-flash)\n")

tts_response = client.text_to_speech.convert(
    text=agent_reply,
    language_code="en-IN",
    speaker="simran_en_sales",
    model="bulbul:v4-flash",
    pace=1.0,
    speech_sample_rate=24000,
    output_audio_codec="mp3",
)

# The SDK returns base64-encoded audio in the 'audios' list
audio_b64 = tts_response.audios[0]
audio_bytes = base64.b64decode(audio_b64)

output_file = "reply.mp3"
with open(output_file, "wb") as f:
    f.write(audio_bytes)

print(f"  Saved voice reply -> {output_file}  ({len(audio_bytes):,} bytes)")
print("\nDone. Play reply.mp3 to hear the agent speak.\n")
