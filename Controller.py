import pandas as pd

from Models.DataVaultEntity import DataVaultEntity
from Models.Model import Model
from CsvProcessor import CsvProcessor

class Controller:
	_instance = None

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		self.model = Model()
		self.csvProcessor = CsvProcessor()

	def get_entities(self):
		return self.model.entities

	def get_source_columns(self):
		return self.model.columns

	def update_entity(self, entity):
		# Ensure the entity is a DataVaultEntity
		if not isinstance(entity, DataVaultEntity):
			raise ValueError("Input entity must be an instance of the DataVaultEntity class.")

		# Find the entity in the model's entities list
		for i, existing_entity in enumerate(self.model.entities):
			if existing_entity.name == entity.name:
				# If found, update the entity
				self.model.entities[i] = entity
				print(f"Entity {entity.name} updated successfully. {entity}")
				return self.model.entities[i]

		# If not found, raise an error
		raise ValueError(f"Entity with name {entity.name} not found.")

	def process_data(self, frame_type, **kwargs):
		frame_method = getattr(self, frame_type, None)
		if frame_method is not None and callable(frame_method):
			frame_method(**kwargs)

	#Frame One Data processing
	def FrameOne(self, **kwargs):
		self.model.filepath = kwargs['file_path']
		self.model.context_text = kwargs['context_text']
		self.model.dataframe = self.csvProcessor.read_csv(self.model.filepath)
		self.model.source_columns = self.csvProcessor.extract_headers_and_data_types(self.model.dataframe)
		self.model.columns = self.csvProcessor.columns
		print(f"Columns: {self.model.columns}")
		print("File path:", self.model.filepath)
		print("Context text:", self.model.context_text)
		print(f"Model Source Columns: {self.model.source_columns}")

	#Frame Two Data processing
	def FrameTwo(self, **kwargs):
		entities = kwargs['entities']
		self.model.entities = entities

