class DataType:
    allowed_values = ["NVARCHAR", "DECIMAL", "INT", "BIGINT", "DATE", "DATETIME", "BIT"]

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value not in self.allowed_values:
            raise ValueError(f"Invalid value. Allowed values are {self.allowed_values}")
        self._value = new_value

    def __repr__(self):
        return f"DataType(value={self._value})"


class Column:
    def __init__(self, source_name, is_primary_key, data_type, business_name):
        self._source_name = source_name
        self._is_primary_key = is_primary_key
        self.data_type = data_type
        self._business_name = business_name

    @property
    def source_name(self):
        return self._source_name

    @source_name.setter
    def source_name(self, value):
        self._source_name = value

    @property
    def is_primary_key(self):
        return self._is_primary_key

    @is_primary_key.setter
    def is_primary_key(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_primary_key must be a boolean.")
        self._is_primary_key = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        if isinstance(value, DataType):
            self._data_type = value
        elif isinstance(value, str):
            self._data_type = DataType(value)
        else:
            raise ValueError("data_type must be a DataType object or a string in DataType.allowed_values.")

    @property
    def business_name(self):
        return self._business_name

    @business_name.setter
    def business_name(self, value):
        self._business_name = value

    def __repr__(self):
        return f"Column(source_name={self._source_name}, is_primary_key={self._is_primary_key}, data_type={self._data_type}, business_name={self._business_name})"
