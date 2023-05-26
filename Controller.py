import pandas as pd
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
		return self.model.source_columns

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
		print("File path:", self.model.filepath)
		print("Context text:", self.model.context_text)
		print(f"Model Source Columns: {self.model.source_columns}")

	#Frame Two Data processing
	def FrameTwo(self, **kwargs):
		entities = kwargs['entities']
		self.model.entities = entities

