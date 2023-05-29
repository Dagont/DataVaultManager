import customtkinter as ctk
import tkinter as tk
from Controller import Controller

ctk.set_appearance_mode("dark")


class FrameFive(ctk.CTkFrame):
	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.controller = Controller()
		self.app = app
		self.regular = ctk.CTkFont(family="Roboto", size=14)
		self.subtle = ctk.CTkFont(family="Roboto", size=12)

		# Row 1
		self.stage_table_name_label = ctk.CTkLabel(
			master=self, text="Stage table name:", font=self.regular
		)
		self.stage_table_name_label.pack(pady=(20, 10))

		self.stage_table_name_input = ctk.CTkEntry(master=self, font=self.regular)
		self.stage_table_name_input.pack(pady=(0, 10))

		# Row 2
		self.file_code_label = ctk.CTkLabel(
			master=self, text="File Code", font=self.regular
		)
		self.file_code_label.pack(pady=(0, 10))

		self.file_code_input = ctk.CTkEntry(master=self, font=self.regular)
		self.file_code_input.pack(pady=(0, 10))

		# Row 3
		self.project_code_label = ctk.CTkLabel(
			master=self, text="Project Code (KPI/JR)", font=self.regular
		)
		self.project_code_label.pack(pady=(0, 10))

		self.project_code_input = ctk.CTkEntry(master=self, font=self.regular)
		self.project_code_input.pack(pady=(0, 10))

	def process_data(self):
		file_code = self.file_code_input.get()
		stage_table_name = self.stage_table_name_input.get()
		project_code = self.project_code_input.get()
		self.controller.process_data("FrameFive", file_code=file_code, stage_table_name=stage_table_name, project_code=project_code)
		self.controller.generate_stage_view_script()
