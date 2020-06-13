import enum
import os
import time
import pystray as pt
import tkinter as tk
import win32api, win32con, win32gui
from PIL import Image
from threading import Thread, Event


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.opacity = 0

        # Maximize and and lock as the top window
        for att in ("-fullscreen", "-topmost", "-disabled"):
            self.attributes(att, True)

        # Windows only
        self.style = (
            win32con.WS_EX_COMPOSITED
            | win32con.WS_EX_LAYERED
            | win32con.WS_EX_NOACTIVATE
            | win32con.WS_EX_TOPMOST
            | win32con.WS_EX_TRANSPARENT
        )

        # Fill the window with a black overlay
        tk.Label(
            self,
            bg="black",
            width=self.winfo_screenwidth(),
            height=self.winfo_screenheight(),
        ).pack()

    def set_opacity(self, val):
        # Set the opacity of the window between 0 [transparent] and 1 [solid]
        self.opacity += val
        self.attributes("-alpha", self.opacity)

    def allow_click_through(self):
        # On windows prevent the mouse from blocking mouse clicks
        handle = win32gui.FindWindow(None, self.title())
        win32api.SetWindowLong(handle, win32con.GWL_EXSTYLE, self.style)


class Fade(Thread):

    increment = 0.005
    speed = 10  # ms
    duration = 20  # sec

    def __init__(self, event):
        # Create thread, Window, and record the time
        Thread.__init__(self)
        self.event = event
        self.window = Window()
        self.start_time = time.time()

    def check_duration(self):
        # Set event if the duration has elapsed
        if time.time() - self.start_time >= self.duration:
            self.event.set()

    def control_fade(self):
        # Change fade direction if upper or lower limit is reached
        if self.window.opacity <= 0:
            self.increment = abs(self.increment)
        elif self.window.opacity >= 0.5:
            self.increment = -self.increment

    def update_opacity(self):
        self.window.set_opacity(self.increment)

    def fade(self):
        self.control_fade()
        self.update_opacity()
        self.window.allow_click_through()
        self.check_duration()

        if self.event.is_set():
            # Kill window and stop thread
            self.window.destroy()
            return
        # Repeat function until event is set
        self.window.after(self.speed, self.fade)

    def start(self):
        # Run thread
        self.fade()
        self.window.mainloop()


class State(enum.IntEnum):
    PAUSED = 0
    ACTIVE = 1


class SysTray:
    def __init__(self):
        self.state = State.ACTIVE
        self.event = Event()

        # Load icon images for app
        self.status_dic = {
            State.PAUSED: Image.open("../icons/paused.png"),
            State.ACTIVE: Image.open("../icons/active.png"),
        }

        # Load menu for app
        self.menu = pt.Menu(
            pt.MenuItem(None, self.left_click, default=True, visible=False),
            pt.MenuItem("exit", self.exit),
        )

    def update_status(self):
        # Match app icon and title to current state
        self.app.icon = self.status_dic[self.state]
        self.app.title = f"20³ ({self.state.name.lower()})"

    def update_time(self):
        self.time = time.time()

    def toggle_state(self):
        self.state = State(not self.state)

    def left_click(self):
        # Function for when the app icon is left clicked by mouse
        self.toggle_state()
        self.update_status()
        if self.state:
            self.event.clear()
            self.update_time()
        else:
            self.event.set()

    def twenty_mins_elapsed(self):
        if time.time() - self.time >= 20 * 61:
            return True

    def worker(self):
        # Background worker to launch screen fading threads
        while True:
            if self.state:
                if self.twenty_mins_elapsed():
                    self.event.clear()
                    Fade(self.event).start()
                    self.update_time()
            time.sleep(0.25)

    def run(self):
        # Create the app with preloaded menu
        self.app = pt.Icon(None, menu=self.menu)
        self.update_status()
        self.update_time()

        # Create worker that will stop if app is closed
        w = Thread(target=self.worker)
        w.setDaemon(True)
        w.start()

        # Start the app
        self.app.run()

    def exit(self):
        self.app.stop()


if __name__ == "__main__":
    app = SysTray()
    app.run()
