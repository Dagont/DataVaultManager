class DataType:
    allowed_values = ["NVARCHAR", "DECIMAL", "INT", "BIGINT", "DATE", "DATETIME", "BIT"]

    def __init__(self, value):
        self._value = None
        self.value = value

    def __eq__(self, other):
        if isinstance(other, DataType):
            return self.value == other.value
        return NotImplemented

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
    def __init__(self, source_name, is_primary_key, is_included, data_type, business_name):
        self._source_name = source_name
        self._is_primary_key = is_primary_key
        self._is_included = is_included
        self.data_type = data_type
        self._business_name = business_name

    def __eq__(self, other):
        if not isinstance(other, Column):
            return False
        return (self.source_name == other.source_name and
                self.is_primary_key == other.is_primary_key and
                self.data_type == other.data_type and
                self.business_name == other.business_name)

    @property
    def source_name(self):
        return self._source_name

    @source_name.setter
    def source_name(self, value):
        self._source_name = value


    @property
    def is_included(self):
        return self._is_included

    @is_included.setter
    def is_included(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_included must be a boolean.")
        self._is_included = value


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
        return f"Column(source_name={self._source_name}, is_pk={self._is_primary_key}, is_incl={self._is_included},data_type={self._data_type}, business_name={self._business_name})"
