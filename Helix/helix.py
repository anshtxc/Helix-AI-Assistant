from gui import AssistantGUI
from listen import listen
from commands import handle_command
from brain import chat_brain
from speak import speak
import threading
import time
import state   # ← added

active_mode = False
gui = AssistantGUI()


def voice_loop():
    global active_mode

    wake_words = ["wake up", "hey helix", "wake up helix"]
    sleep_words = ["stop", "sleep", "standby"]

    while True:
        cmd = listen()

        if not cmd:
            time.sleep(0.05)
            continue

        cmd_lower = cmd.lower()

        # WAKE
        if any(w in cmd_lower for w in wake_words):
            if not active_mode:
                active_mode = True
                state.awake = True
                gui.root.after(0, gui.set_active, True)

                #  SECURITY CHECK
                if state.locked:
                    state.awaiting_password = True
                    speak("I am awake Sir. Voice recognition required.")
                else:
                    speak("I am awake Sir. Awaiting your command.")
            continue

        # SLEEP
        if any(w in cmd_lower for w in sleep_words):
            active_mode = False
            state.awake = False
            gui.root.after(0, gui.set_active, False)
            speak("Going in standby mode Sir.")
            continue

        # COMMAND MODE
        if active_mode:
            gui.root.after(0, gui.update_command, cmd)

            handled = handle_command(cmd, gui)

            if not handled:
                reply = chat_brain(cmd)
                speak(reply)


def start_loop():
    threading.Thread(target=voice_loop, daemon=True).start()


start_loop()
gui.run()