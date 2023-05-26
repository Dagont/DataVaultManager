import customtkinter as ctk
import tkinter as tk
import GUI_FrameTwo
from tkinter import filedialog
from Controller import Controller

ctk.set_appearance_mode("dark")

class FrameOne(ctk.CTkFrame):
    def __init__(self, app, *args, header_name="RadioButtonFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = Controller()
        self.app = app
        self.regular = ctk.CTkFont(family="Roboto", size=14)
        self.subtle = ctk.CTkFont(family="Roboto", size=12)
        self.file_path = None
        self.header_name = header_name

        # Row 1
        self.select_file_label = ctk.CTkLabel(
            master=self, text="Select file to load into DataVault 2.0", font=self.regular
        )
        self.select_file_label.pack(pady=(20, 10))

        # Row 2
        self.load_file_btn = ctk.CTkButton(
            master=self, text="Load File", command=self.select_file, font=self.regular
        )
        self.load_file_btn.pack(pady=(0, 10))

        # Row 3
        self.file_name_label = ctk.CTkLabel(master=self, text="", font=self.subtle, text_color="#acacac")
        self.file_name_label.pack(pady=(0, 10))

        # Row 4
        self.separator = ctk.CTkLabel(master=self, text="", font=self.regular)
        self.separator.pack(pady=(0, 10))

        # Row 5
        self.add_context_label = ctk.CTkLabel(
            master=self, text="Add context, what is the file about?", font=self.regular
        )
        self.add_context_label.pack(pady=(0, 10))

        # Row 6
        self.context_entry = ctk.CTkTextbox(master=self, font=self.regular, width=420, height=100)
        self.context_entry.pack(pady=(0, 10))

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.master.file_path = self.file_path
            file_name = self.file_path.split("/")[-1]
            self.file_name_label.configure(text="Selected : " + file_name)

    def process_data(self):
        file_path = self.file_path
        context_text = self.context_entry.get("1.0", tk.END).strip()
        self.controller.process_data("FrameOne", file_path=file_path, context_text=context_text)



