import customtkinter as ctk
import tkinter as tk
from Controller import Controller

from Models.EntityRelationship import EntityRelationship

ctk.set_appearance_mode("dark")


class RelationsDefinition(ctk.CTkFrame):
	def __init__(self, frame_three, *args, entities=[], combobox1_options=[], combobox2_options=[], **kwargs):
		super().__init__(*args, **kwargs)
		self.frame_three = frame_three
		self.combobox1_options = combobox1_options
		self.combobox2_options = combobox2_options
		self.entities = entities
		self.create_widgets()

	def create_widgets(self):
		self.combobox1 = ctk.CTkComboBox(master=self, values=self.combobox1_options, state="readonly")
		self.combobox1.pack(side="left", padx=(0, 10))

		self.label = ctk.CTkLabel(master=self, text="<=>")
		self.label.pack(side="left", padx=(0, 10))

		self.combobox2 = ctk.CTkComboBox(master=self, values=self.combobox2_options, state="readonly")
		self.combobox2.pack(side="left", padx=(0, 10))
		delete_button = ctk.CTkButton(master=self, text="Delete", command=self.delete_element)
		delete_button.pack(side="left", padx=(0, 50))

	def delete_element(self):
		self.frame_three.relations_definitions.remove(self)
		self.destroy()

	def get_entity_relationship(self):
		entity1_label = self.combobox1.get()
		entity2_label = self.combobox2.get()

		entity1 = next((entity for entity in self.entities if entity.name == entity1_label), None)
		entity2 = next((entity for entity in self.entities if entity.name == entity2_label), None)
		if entity1 is not None and entity2 is not None:
			return EntityRelationship(entity1, entity2)

		return None


class FrameThree(ctk.CTkFrame):
	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.create_widgets()
		self.controller = Controller()
		self.relations_definitions = []
		self.entity_relationships = []

	def create_widgets(self):
		self.title_label = ctk.CTkLabel(master=self, text="Relaciones entre Entidades")
		self.title_label.pack(pady=(20, 10))

		self.scrollable_relations_frame = ctk.CTkScrollableFrame(self, width=580, height=200)
		self.scrollable_relations_frame.pack(pady=(0, 10), fill="both", expand=True)

		self.add_new_btn = ctk.CTkButton(master=self, text="Add new", command=self.add_new_relations_definition)
		self.add_new_btn.pack(pady=(0, 20))

	def add_new_relations_definition(self):
		try:
			entities = self.controller.get_entities()
			print(entities)
			combobox1_options = [entity.name for entity in entities if entity.is_link]
			combobox2_options = [entity.name for entity in entities if entity.is_hub or entity.is_sat]
			relations_def = RelationsDefinition(self, self.scrollable_relations_frame, entities=entities, combobox1_options=combobox1_options, combobox2_options=combobox2_options)
			relations_def.pack(pady=(0, 5))
			self.relations_definitions.append(relations_def)
		except tk.TclError as e:
			print(f"An error occurred: {e}")

	def process_data(self):
		self.entity_relationships = []
		for relations_def in self.relations_definitions:
			entity_relationship = relations_def.get_entity_relationship()
			if entity_relationship is not None:
				self.entity_relationships.append(entity_relationship)
		#print(self.entity_relationships)
		self.controller.process_data("FrameThree", entity_relationships=self.entity_relationships)
