import customtkinter as tk
import threading

class AppInterface:
    def __init__(self):
        self.root = tk.CTk()
        self.root.geometry('1920X1080')
        
        self.screen = tk.CTkLabel(self.root, text='', width=1920, height=1080)
        self.screen.pack()

    def update_screen(self, img):
        self.screen.forget()
        self.screen.configure(image=img)
        self.screen.pack()
    
    def get_root_cordinates(self):
        return self.root.winfo_rootx(), self.root.winfo_rooty()
    
    def start(self):
        # Run app
        self.root.mainloop()
        