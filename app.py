from gui.upload_scene import UploadScene
import tkinter

class App():
    def __init__(self):
        self.upload_scene = UploadScene()
        
    def start(self):
        self.root = tkinter.Tk()
        self.root.title = "Company Expenses"
        self.root.geometry("1024x576")

        self.show_upload_scene()

        self.root.mainloop()

    def show_upload_scene(self):
        self.upload_scene.show(self)

if __name__ == "__main__":
    App().start()
