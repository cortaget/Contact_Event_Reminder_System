import customtkinter as ctk


class BaseScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        self.grid_forget()
