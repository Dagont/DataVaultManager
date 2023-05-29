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
				for column in self.model.entities[i].columns:
					print(f"{column.source_name} -> included: {column.is_included}  primary:{column.is_primary_key}")
				print(f"Entity {entity.name} pk: {entity.get_primary_key_columns()}")
				print(f"Entity {entity.name} incl: {entity.get_included_columns()}")
				return self.model.entities[i]

		# If not found, raise an error
		raise ValueError(f"Entity with name {entity.name} not found.")

	def process_data(self, frame_type, **kwargs):
		frame_method = getattr(self, frame_type, None)
		if frame_method is not None and callable(frame_method):
			frame_method(**kwargs)

	# Frame One Data processing
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

	# Frame Two Data processing
	def FrameTwo(self, **kwargs):
		existing_entities = self.model.entities
		incoming_entities = kwargs['entities']

		# Case for incoming entities
		for new_entity in incoming_entities:
			if any(entity.name == new_entity.name for entity in existing_entities):
				print(f"Entity with name '{new_entity.name}' already exists. Skipping.")
				continue
			else:
				self.model.add_entity(new_entity)

		# Case for deletion of existing entities
		for existing_entity in existing_entities:
			if not any(entity.name == existing_entity.name for entity in incoming_entities):
				self.model.delete_entity(existing_entity)

	def FrameThree(self, **kwargs):
		entity_relationships = kwargs['entity_relationships']
		self.model.entities_relationships = entity_relationships

	def FrameFive(self, **kwargs):
		file_code = kwargs['file_code']
		stage_table_name = kwargs['stage_table_name']
		project_code = kwargs['project_code']
		self.model.file_code = file_code
		self.model.stage_table_name = stage_table_name
		self.model.project_code = project_code
		print(f"Set filecode: {self.model.file_code}")
		print(f"Set stagetablename: {self.model.stage_table_name}")


	def generate_hashkey_segment(self, entity):
		print("Generating hashkey")
		hashkey_segment = ""
		pk_cols = entity.get_primary_key_columns()
		print(f"pk_cols: {pk_cols}")
		if not (entity.is_hub or entity.is_link):
			return ""

		hashkey_segment += f"\n\t-- Primary Key of the {'Hub' if entity.is_hub else 'Link'} {entity.name} --\n"

		if entity.count_primary_key_columns() == 0:
			hashkey_segment += f"\tHashBytes('SHA2_256',\n\tCONCAT(\n\t\tNEWID(),'|'\n\t)) AS {entity.prefix}_{entity.name}_PK,\n"
		if entity.count_primary_key_columns() == 1:
			hashkey_segment += f"\tHashBytes('SHA2_256',\n\tCONCAT(\n\t\tSTG.CleanCol([{entity.get_primary_key_columns()[0].source_name}]),'|'\n\t)) AS {entity.prefix}_{entity.name}_PK,\n"
		if entity.count_primary_key_columns() > 1:
			hashkey_segment += f"\tHashBytes('SHA2_256',\n\tCONCAT("
			for column in pk_cols:
				hashkey_segment += f"\n\t\tSTG.CleanCol([{column.source_name}]),'|',"
			hashkey_segment = hashkey_segment.rsplit(',', 1)[0]
			hashkey_segment += f"\n\t)) AS {entity.prefix}_{entity.name}_PK,\n\n"

		return hashkey_segment

	def generate_hashdiff_segment(self, entity):
		print("Generating hashdiff")

		hashdiff_segment = f"\n\t-- Hash diff of the satellite {entity.name} --\n"
		included_cols = entity.get_included_columns()
		print(f"included_cols {included_cols}")
		if not entity.is_sat:
			return ""

		if len(included_cols) == 1:
			hashdiff_segment += f"\tHashBytes('SHA2_256',\n\tCONCAT(\n\t\tSTG.CleanCol([{entity.get_primary_key_columns()[0].source_name}]),'|'\n\t)) AS {entity.prefix}_{entity.name}_PK,\n"
		if len(included_cols) > 1:
			hashdiff_segment += f"\tHashBytes('SHA2_256',\n\tCONCAT("
			for column in included_cols:
				hashdiff_segment += f"\n\t\tSTG.CleanCol([{column.source_name}]),'|',"
			hashdiff_segment = hashdiff_segment.rsplit(',', 1)[0]
			hashdiff_segment += f"\n\t)) AS HashDiff_S_{entity.name},\n\n"

		return hashdiff_segment

	def generate_stage_view_script(self):
		source_columns = self.model.columns
		entities = self.model.entities
		entity_relationships = self.model.entities_relationships
		stage_table_name = self.model.stage_table_name
		file_code = self.model.file_code
		project_code = self.model.project_code


		stage_script = f"CREATE VIEW [STG].[Vw_{project_code}_{stage_table_name}__{file_code}] AS\n\tSELECT\n\t-- Columnas Origen --\n"

		# Add source columns to the script
		for column in source_columns:
			stage_script += f"\t[{column.source_name}],\n"

		# Add control columns to the script
		stage_script += f"\t-- Columnas de Control --\n\tGETDATE() AS Fecha_Actual,\n\t'[STG].[{stage_table_name}]' AS Sistema_Tabla,\n"

		for entity in entities:
			print(f"Processing {entity}")
			stage_script += self.generate_hashkey_segment(entity)
			stage_script += self.generate_hashdiff_segment(entity)

		print(stage_script)
		self.save_string_to_file(stage_script, "test.txt")

		return stage_script

	def save_string_to_file(self, content, filename):
		with open(filename, 'w') as file:
			file.write(content)
