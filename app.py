from gui.upload_scene import UploadScene
from gui.entries_scene import EntriesScene
import tkinter
from managers.database import Database

class App:
    def __init__(self):
        self.entries_scene = EntriesScene()

    def start(self):
        self.root = tkinter.Tk()
        self.root.title = "Company Expenses"
        self.root.geometry("1024x576")
        
        self.show_entries_scene()
        self.root.mainloop()

    def show_entries_scene(self):
        self.entries_scene.show(self)

if __name__ == "__main__":
    App().start()
