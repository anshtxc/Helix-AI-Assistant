from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import threading

from listen import listen
from commands import handle_command
from brain import chat_brain
from speak import speak

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

active=False


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


def voice_loop():
    global active

    while True:

        if not active:
            continue

        cmd = listen()
        if not cmd:
            continue

        socketio.emit("heard",cmd)

        handled = handle_command(cmd,None)

        if not handled:
            reply = chat_brain(cmd)
            speak(reply)
            socketio.emit("reply",reply)


@socketio.on("start")
def start():
    global active
    active=True
    emit("status","Listening",broadcast=True)
    socketio.emit("animate",True)


@socketio.on("stop")
def stop():
    global active
    active=False
    emit("status","Stopped",broadcast=True)
    socketio.emit("animate",False)


threading.Thread(target=voice_loop,daemon=True).start()

if __name__=="__main__":
    socketio.run(app,port=5000)