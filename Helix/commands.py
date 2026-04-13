from speak import speak
from actions import *
import datetime
import state
from memory import remember, recall

def parse_site_command(command):
    command = command.replace("and", "")
    words = command.split()

    site = None
    query = None

    if "open" in words:
        idx = words.index("open")
        if idx + 1 < len(words):
            site = words[idx + 1]

    if "search" in words:
        idx = words.index("search")
        query = " ".join(words[idx + 1:])

    if "play" in words:
        idx = words.index("play")
        query = " ".join(words[idx + 1:])

    return site, query


def handle_command(cmd, gui):

    print("HANDLE CMD RECEIVED:", cmd)
    command = cmd.lower()
   
    if "stop" in command or "quiet" in command or "silence" in command:
        import state
        state.stop_speaking = True
        speak("Okay Sir")
        return True
    
    if "remember that" in command:
        fact = command.replace("remember that", "").strip()
        remember("note", fact)
        speak("I will remember that Sir.")
        return True
    
    if "what did i tell you" in command:
        note = recall("note")
        if note:
            speak(f"You told me {note}")
        else:
            speak("You have not told me anything to remember yet Sir.")
        return True
    
    if "my name is" in command:
        name = command.replace("my name is", "").strip()
        remember("user_name", name)
        speak(f"Nice to meet you {name} Sir.")
        return True

    if "what is my name" in command:
        name = recall("user_name")
        if name:
            speak(f"Your name is {name} Sir.")
        else:
            speak("You have not told me your name yet Sir.")
        return True




    # Greetings
    if "hello" in command:
        speak("hello Sir, i am ready to assist your commands.")
        return True

    if "how are you" in command or "howru" in command:
        speak("I am functioning perfectly, Sir.")
        return True

    if "wake up" in command:
        speak("I am awake, Sir.")
        return True
    
    if "who made you" in command:
        speak("i am made by ansh sir, a personal AI Assistant developed for making your life easier ")
        return True
    
    if "who is ayush" in command:
        speak("ayush is ansh sir's brother")
        return True
    
    if "who r u" in command:
        speak("i am helix, A advance AI assistant made by ansh sir")
        return True
    
    if "who are you" in command:
        speak("i am helix, A personal AI assistant made by ansh sir")
        return True

    if "who is ansh" in command:
        speak("Ansh sir is a grate personality who made me")
        return True
    
    if "who is kanchan" in command:
        speak("Kanchan mam is Ansh's sir girlfrind, he loves her more than anything")
        return True
    
    # Battery
    if "battery" in command:
        speak(get_battery_status())
        return True

    #  Time
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True

    #  Volume controls
    if "increase volume" in command or "volume up" in command:
        volume_up()
        speak("Volume increased")
        return True

    if "decrease volume" in command or "volume down" in command:
        volume_down()
        speak("Volume decreased")
        return True

    if "set volume" in command:
        nums = [int(s) for s in command.split() if s.isdigit()]
        if nums:
            set_volume(nums[0])
            speak(f"Volume set to {nums[0]} percent")
        else:
            speak("Please tell a volume level")
        return True

    # Screenshot
    if "screenshot" in command:
        take_screenshot()
        speak("Screenshot taken")
        return True

    #  Lock
    if "lock" in command:
        lock_pc()
        speak("Computer locked")
        return True

    #Shutdown
    if "shutdown" in command:
        speak("Shutting down the system")
        shutdown_pc()
        return True
    
    if command.startswith(("close", "exit", "terminate")):

        words = command.split()
    
        if len(words) < 2:
            speak("Tell me which app to close")
            return True

        app = " ".join(words[1:])

        if close_app(app):
            speak(f"{app} closed")
        else:
            speak(f"{app} is not running")
  
        return True

    #  Open app / website
    if command.startswith("open"):
        name = command.replace("open", "").strip()
        open_anything(name)
        speak(f"Opening {name}")
        return True
    
    if "open" in command or "play" in command:
        site, query = parse_site_command(command)

        if site:
            open_site(site, query)
            if query:
                speak(f"Opening {site} and searching {query}")
            else:
                speak(f"Opening {site}")
            return True