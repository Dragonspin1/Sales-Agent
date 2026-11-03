"""
sarvam_test.py
--------------
Minimal smoke-test: initialise the Sarvam client and make one
chat-completion call using sarvam-m.
The API key is read from the SARVAM_API_KEY environment variable
(loaded from .env via python-dotenv).
"""

import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

# Load .env → environment
load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    raise EnvironmentError(
        "SARVAM_API_KEY is not set. "
        "Add it to your .env file and try again."
    )

# Initialise client
client = SarvamAI(api_subscription_key=api_key)

# One chat-completion call
response = client.chat.completions(
    messages=[
        {"role": "user", "content": "Hello! In one sentence, what can you do?"}
    ],
    model="sarvam-105b-conversations",
)

# Print the reply
print("Sarvam reply:", response.choices[0].message.content)
