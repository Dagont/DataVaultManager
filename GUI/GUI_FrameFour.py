import copy

import customtkinter as ctk
from tkinter import ttk
from Controller import Controller
from Models.Column import DataType

ctk.set_appearance_mode("dark")


class RowDefinition(ctk.CTkFrame):
	def __init__(self, *args,  column=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.business_name_entry = None
		self.datatype_combobox = None
		self.pk_checkbox = None
		self.add_checkbox = None
		self.label = None
		self.column = column
		self.is_included = ctk.BooleanVar(value=False)
		self.is_pk = ctk.BooleanVar(value=False)
		self.create_widgets()

	def create_widgets(self):

		self.label = ctk.CTkLabel(master=self, text=self.column.source_name, width=100)
		self.label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

		self.add_checkbox = ctk.CTkCheckBox(master=self, text="", onvalue=True, offvalue=False, variable=self.is_included)
		self.add_checkbox.grid(row=0, column=1, padx=(100, 5), pady=(5, 5))

		self.pk_checkbox = ctk.CTkCheckBox(master=self, text="", onvalue=True, offvalue=False, variable=self.is_pk)
		self.pk_checkbox.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

		self.datatype_combobox = ctk.CTkComboBox(master=self, state="readonly", values=["NVARCHAR", "DECIMAL", "INT", "BIGINT", "DATE", "DATETIME", "BIT"])
		self.datatype_combobox.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

		self.business_name_entry = ctk.CTkEntry(master=self)
		self.business_name_entry.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

		if self.column is not None:
			self.is_pk = ctk.BooleanVar(value=self.column.is_primary_key)
			self.pk_checkbox.configure(variable=self.is_pk)
			self.datatype_combobox.set(self.column.data_type.value)
			if self.column.business_name is None:
				self.column.business_name = ""
			self.business_name_entry.insert(0, self.column.business_name)


class FrameFour(ctk.CTkFrame):
	def __init__(self, app, entity, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.controller = Controller()
		self.entity = entity

		# Row 1
		entity_label = ctk.CTkLabel(master=self, text=f"Entidad: {self.entity.name}")
		entity_label.pack(pady=(20, 10))

		# Row 2
		header_frame = ctk.CTkFrame(master=self)
		header_frame.pack(pady=(10, 10))

		header_label1 = ctk.CTkLabel(master=header_frame, text="Column", width=200)
		header_label1.grid(row=0, column=0, padx=(0, 20), sticky="w")

		header_label2 = ctk.CTkLabel(master=header_frame, text="Add?")
		header_label2.grid(row=0, column=1, padx=(0, 40), sticky="w")

		header_label3 = ctk.CTkLabel(master=header_frame, text="is PK?")
		header_label3.grid(row=0, column=2, padx=(40, 40), sticky="w")

		header_label4 = ctk.CTkLabel(master=header_frame, text="DataType")
		header_label4.grid(row=0, column=3, padx=(40, 40), sticky="w")

		header_label5 = ctk.CTkLabel(master=header_frame, text="BusinessName")
		header_label5.grid(row=0, column=4, padx=(40, 40), sticky="w")

		# Row 3
		self.scrollable_row_definitions_frame = ctk.CTkScrollableFrame(self, width=780, height=200)
		self.scrollable_row_definitions_frame.pack(pady=(0, 10), fill="both", expand=True)

		if not self.entity.columns:
			self.entity.columns = copy.deepcopy(self.controller.get_source_columns())

		for column in self.entity.columns:
			row_definition = RowDefinition(self.scrollable_row_definitions_frame, column=column)
			row_definition.pack(pady=(0, 5))

	def process_data(self):
		self.update_entity()

	"""def update_entity(self):
		for i, row_definition in enumerate(self.scrollable_row_definitions_frame.children.values()):
			if isinstance(row_definition, RowDefinition):
				column = self.entity.columns[i]
				column.is_included = row_definition.is_included.get()
				column.is_primary_key = row_definition.is_pk.get()
				column.data_type = DataType(row_definition.datatype_combobox.get())
				column.business_name = row_definition.business_name_entry.get()

		self.controller.update_entity(self.entity)"""

	def update_entity(self):
		for row_definition in self.scrollable_row_definitions_frame.children.values():
			if isinstance(row_definition, RowDefinition):
				column = next((col for col in self.entity.columns if col.source_name == row_definition.label.cget("text")), None)
				if column is not None:
					column.is_included = row_definition.is_included.get()
					column.is_primary_key = row_definition.is_pk.get()
					column.data_type = DataType(row_definition.datatype_combobox.get())
					column.business_name = row_definition.business_name_entry.get()

		self.controller.update_entity(self.entity)

