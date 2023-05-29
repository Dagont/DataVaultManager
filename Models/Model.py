from Models.DataVaultEntity import DataVaultEntity
from Models.EntityRelationship import EntityRelationship


class SQLServerCode:
    def __init__(self):
        self.stageViewScript = ""
        self.rawVaultTableScripts = ""
        self.rawVaultSPScript = ""
        self.businessVaultTableScripts = ""
        self.businessVaultSPScript = ""
        self.informationMartScript = ""

class Model:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize the instance attributes
            cls._instance.filepath = None
            cls._instance.context_text = None
            cls._instance.entities = []
            cls._instance.entities_relationships = []
            cls._instance.source_columns = []
            cls._instance.dataframe = []
            cls._instance.columns = []
            cls._instance.file_code = None
            cls._instance.project_code = None
            cls._instance.stage_table_name = None
            cls._instance.sql_server_code = SQLServerCode()
        return cls._instance


    @property
    def project_code(self):
        return self._project_code

    @project_code.setter
    def project_code(self, value):
        self._project_code = value
    @property
    def file_code(self):
        return self._file_code

    @file_code.setter
    def file_code(self, value):
        self._file_code = value

    @property
    def stage_table_name(self):
        return self._stage_table_name

    @stage_table_name.setter
    def stage_table_name(self, value):
        self._stage_table_name = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value

    @property
    def source_columns(self):
        return self._source_columns

    @source_columns.setter
    def source_columns(self, value):
        self._source_columns = value

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    @property
    def context_text(self):
        return self._context_text

    @context_text.setter
    def context_text(self, value):
        self._context_text = value

    @property
    def entities(self):
        return self._entities

    def add_entity(self, entity):
        if isinstance(entity, DataVaultEntity):
            self._entities.append(entity)
        else:
            raise ValueError("Entity must be an instance of the DataVaultEntity class.")

    def delete_entity(self, entity):
        if isinstance(entity, DataVaultEntity):
            self._entities.remove(entity)
        else:
            raise ValueError("Entity must be an instance of the DataVaultEntity class.")

    @entities.setter
    def entities(self, value):
        if all(isinstance(entity, DataVaultEntity) for entity in value):
            self._entities = value
        else:
            raise ValueError("All elements of 'entities' must be instances of the DataVaultEntity class.")

    @property
    def entities_relationships(self):
        return self._entities_relationships

    @entities_relationships.setter
    def entities_relationships(self, value):
        if all(isinstance(rel, EntityRelationship) for rel in value):
            self._entities_relationships = value
        else:
            raise ValueError("All elements of 'entities_relationships' must be instances of the EntityRelationship class.")

    def add_relationship(self, entity1, entity2=None):
        if entity2 is None:
            # entity1 is actually a relationship
            relationship = entity1
        else:
            # entity1 and entity2 are entities
            relationship = EntityRelationship(entity1, entity2)

        if isinstance(relationship, EntityRelationship):
            self._entities_relationships.append(relationship)
        else:
            raise ValueError("Invalid argument. Expected an EntityRelationship instance or two DataVaultEntity instances.")

    def delete_relationship(self, relationship):
        if isinstance(relationship, EntityRelationship):
            self._entities_relationships.remove(relationship)
        else:
            raise ValueError("Relationship must be an instance of the EntityRelationship class.")
