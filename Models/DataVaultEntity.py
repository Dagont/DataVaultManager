from Models.Column import Column


class DataVaultEntity:
    def __init__(self, name, is_hub, is_sat, is_link, columns=None):
        self._name = name
        self._is_hub = is_hub
        self._is_sat = is_sat
        self._is_link = is_link
        if columns is None:
            self._columns = []
        else:
            if all(isinstance(column, Column) for column in columns):
                self._columns = columns
            else:
                raise ValueError("All elements of 'columns' must be instances of the Column class.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def is_hub(self):
        return self._is_hub

    @is_hub.setter
    def is_hub(self, value):
        self._is_hub = value

    @property
    def is_sat(self):
        return self._is_sat

    @is_sat.setter
    def is_sat(self, value):
        self._is_sat = value

    @property
    def is_link(self):
        return self._is_link

    @is_link.setter
    def is_link(self, value):
        self._is_link = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        if all(isinstance(column, Column) for column in value):
            self._columns = value
        else:
            raise ValueError("All elements of 'columns' must be instances of the Column class.")

    def __repr__(self):
        return f"DataVaultEntity(name={self._name}, is_hub={self._is_hub}, is_sat={self._is_sat}, is_link={self._is_link}, columns={self._columns})"
