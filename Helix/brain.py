import requests
import re
from memory import load_memory
import state

cache = {}

OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

memory = [
    {
        "role": "system",
        "content": (
            "You are Helix, a voice-based AI assistant created by Ansh Sir. "
            "Always speak respectfully in Hindi using 'aap', never 'tum'. "
            "If asked who created you, always say: I was made by Ansh sir in 2026. "
            "Detect the user's language automatically. "
            "If the user speaks Hindi, reply fully in Hindi. "
            "If the user speaks English, reply fully in English. "
            "Do not mix languages unless the user does. "
            "Respond in clear spoken sentences only. "
            "Do NOT use emojis, symbols, lists, or formatting. "
            "Keep responses short and natural for voice output."
        )
    }
]

def clean_text(text):
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def force_respect(text):
    replacements = {
        "tum": "aap",
        "Tum": "Aap",
        "tera": "aapka",
        "tere": "aapke",
        "tujhe": "aapko"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def handle_auth(user_text):

    if not state.locked:
        return None

    data = load_memory()
    password = data.get("voice_password", "").lower()

    # waiting for password after wake
    if state.awaiting_password:

        if user_text.lower().strip() == password:
            state.locked = False
            state.awaiting_password = False

            return "Authentication successfull. Welcome back Sir. All systems are now available."

        else:
            return "Incorrect password. Access denied."

    # ignore commands while locked if password not requested yet
    return "System is locked Sir. Say wake up to begin authentication."

def chat_brain(user_text):

    # SECURITY LAYER
    auth = handle_auth(user_text)
    if auth:
        return auth
    key = user_text.strip().lower()

    # Direct override (fast response, no API call needed)
    if "kisne banaya" in key or "who made you" in key or "who created you" in key:
        return "I was made by Ansh sir in 2026."

    if key in cache:
        return cache[key]

    memory.append({"role": "user", "content": user_text})

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": memory[-12:],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()

        reply = clean_text(r.json()["choices"][0]["message"]["content"])
        reply = force_respect(reply)   # Always enforce "aap"

        memory.append({"role": "assistant", "content": reply})
        cache[key] = reply

        return reply

    except Exception:
        return "Maaf kijiye Sir, response thoda slow ho gaya."