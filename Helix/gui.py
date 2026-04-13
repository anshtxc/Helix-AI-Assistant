import tkinter as tk

class AssistantGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Helix AI")
        self.root.geometry("800x500")
        self.root.configure(bg="#0f141f")
        self.root.resizable(False, False)

        # ===== CENTER FRAME =====
        self.frame = tk.Frame(self.root, bg="#0f141f")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # ===== SMALL HELIX TITLE =====
        self.title = tk.Label(
            self.frame,
            text="HELIX",
            fg="#00e5ff",
            bg="#0f141f",
            font=("Segoe UI", 32, "bold")
        )
        self.title.pack(pady=(0, 5))

        # ===== TAGLINE =====
        self.tagline = tk.Label(
            self.frame,
            text="Advanced Personal AI assistant",
            fg="#8a9db0",
            bg="#0f141f",
            font=("Segoe UI", 11)
        )
        self.tagline.pack(pady=(0, 25))

        # ===== STATUS =====
        self.status = tk.Label(
            self.frame,
            text="STOPPED",
            fg="red",
            bg="#0f141f",
            font=("Segoe UI", 10, "bold")
        )
        self.status.pack(pady=5)

        # ===== START / STOP BUTTON =====
        self.button = tk.Button(
            self.frame,
            text="START",
            bg="#00ff88",
            fg="black",
            activebackground="#00cc6a",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            width=14,
            height=1,
            bd=0,
            command=self.toggle
        )
        self.button.pack(pady=15)

        # ===== LAST COMMAND =====
        self.last_command = tk.Label(
            self.frame,
            text="Awaiting command...",
            fg="#00e5ff",
            bg="#0f141f",
            font=("Consolas", 10)
        )
        self.last_command.pack(pady=(10, 0))

        self.active = False

    # ==========================
    # BUTTON TOGGLE
    # ==========================
    def toggle(self):
        if not self.active:
            self.active = True
            self.set_active(True)
            if hasattr(self, "start_listening"):
                self.start_listening()
        else:
            self.active = False
            self.set_active(False)
            if hasattr(self, "stop_listening"):
                self.stop_listening()

    # ==========================
    # STATUS CONTROL
    # ==========================
    def set_active(self, state):
        if state:
            self.button.config(text="STOP", bg="#ff3b3b")
            self.status.config(text="LISTENING", fg="#00ff88")
        else:
            self.button.config(text="START", bg="#00ff88")
            self.status.config(text="STOPPED", fg="red")

    # ==========================
    # UPDATE COMMAND
    # ==========================
    def update_command(self, text):
        self.last_command.config(text=f"> {text}")

    def run(self):
        self.root.mainloop()