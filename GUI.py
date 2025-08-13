import customtkinter as tk
import threading

class AppInterface:
    def __init__(self, width, height):
        self.root = tk.CTk()
        self.root.geometry(f'{width}x{height}')
        
        self.screen = tk.CTkLabel(self.root, text='', width=width, height=height)
        self.screen.pack()

        # Run app
        self.root.mainloop()

    def update_screen(self, img):
        self.screen.forget()
        self.screen.configure(image=img)
        self.screen.pack()
    
    def get_root_cordinates(self):
        return self.root.winfo_rootx(), self.root.winfo_rooty()

        