import customtkinter as ctk
import tkinter as tk
from typing import List, Callable

class CustomListbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 100,
                 select_command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.configure(fg_color=("gray78", "gray28"))  # set frame color
        self.select_command = select_command

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self, width=width-4, height=height-4)
        self.listbox.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def on_select(self, event):
        if self.select_command is not None:
            self.select_command()

    def insert(self, index, *elements):
        for element in elements:
            self.listbox.insert(index, element)
            index += 1

    def delete(self, start, end=None):
        self.listbox.delete(start, end)

    def get(self, start, end=None) -> List[str]:
        return self.listbox.get(start, end)

    def curselection(self):
        return self.listbox.curselection()

    def size(self) -> int:
        return self.listbox.size()
