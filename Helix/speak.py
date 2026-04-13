import edge_tts
import pygame
import threading
import asyncio
import state
import os

VOICE_EN = "en-GB-RyanNeural"
VOICE_HI = "hi-IN-MadhurNeural"

RATE = "-15%"
PITCH = "-15Hz"

pygame.mixer.init()


# ---------------- LANGUAGE DETECTOR ---------------- #
def detect_hindi(text):

    hindi_words = {
        "hai","kya","kaise","haan","nahi","kyun",
        "aap","mera","bolo","namaste","kar","raha",
        "theek","acha","sun","bata","mein","se"
    }

    t = text.lower().strip()

    # detect devanagari characters
    for c in t:
        if "\u0900" <= c <= "\u097F":
            return True

    # split into real words
    words = t.split()

    # check full-word match only
    for w in words:
        if w in hindi_words:
            return True

    return False


# ---------------- VOICE GENERATOR ---------------- #
def generate_voice(text, file, lang=None):

    async def task():

        # language override
        if lang == "en":
            voice = VOICE_EN

        elif lang == "hi":
            voice = VOICE_HI

        else:
            if detect_hindi(text):
                voice = VOICE_HI
            else:
                voice = VOICE_EN

        tts = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=RATE,
            pitch=PITCH
        )

        await tts.save(file)

    asyncio.run(task())


# ---------------- SPEAK FUNCTION ---------------- #
def speak(text, lang=None):

    def run():

        state.is_speaking = True
        file = "voice.mp3"

        try:
            generate_voice(text, file, lang)

            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

            clock = pygame.time.Clock()

            while pygame.mixer.music.get_busy():
                clock.tick(10)

            pygame.mixer.music.unload()

        except Exception as e:
            print("Speak Error:", e)

        finally:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except:
                pass

            state.is_speaking = False

    threading.Thread(target=run, daemon=True).start()