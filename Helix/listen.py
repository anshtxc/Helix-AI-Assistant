import speech_recognition as sr
import state

r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True


def listen():
    if state.is_speaking:
        return ""

    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
        except:
            return ""

    try:
        return r.recognize_google(audio, language="en-IN").lower()
    except:
        return ""