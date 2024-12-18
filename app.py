import tkinter as tk
from gui.entries_scene import EntriesScene

class App:
    def __init__(self):
        self.entries_scene = EntriesScene()

    def start(self):
        self.root = tk.Tk()
        self.root.title("Company Expenses")
        self.root.geometry("1024x576")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_entries_scene()
        self.root.mainloop()

    def show_entries_scene(self):
        self.entries_scene.show(self)

    def on_closing(self):
        if hasattr(self, "connection") and self.connection:
            self.connection.close()

        self.root.destroy()

if __name__ == "__main__":
    App().start()
