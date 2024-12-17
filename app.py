import os
from gui.upload_scene import UploadScene
from gui.entries_scene import EntriesScene
import tkinter
from managers.database import Database

class App:
    def __init__(self):
        self.upload_scene = UploadScene()
        self.entries_scene = EntriesScene()

        self.database = Database()

    def start(self):
        self.root = tkinter.Tk()
        self.root.title = "Company Expenses"
        self.root.geometry("1024x576")

        if not os.path.exists(self.database.db_filename):
            self.show_upload_scene()
        else:
            self.show_entries_scene()

        self.root.mainloop()

    def show_upload_scene(self):
        self.upload_scene.show(self)

    def show_entries_scene(self):
        self.entries_scene.show(self)

if __name__ == "__main__":
    App().start()
