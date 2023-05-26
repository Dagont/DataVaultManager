from Models.DataVaultEntity import DataVaultEntity


class Model:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize the instance attributes
            cls._instance.filepath = None
            cls._instance.context_text = None
            cls._instance.entities = []
            cls._instance.source_columns = []
            cls._instance.dataframe = []
        return cls._instance

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

    @entities.setter
    def entities(self, value):
        if all(isinstance(entity, DataVaultEntity) for entity in value):
            self._entities = value
        else:
            raise ValueError("All elements of 'entities' must be instances of the DataVaultEntity class.")
