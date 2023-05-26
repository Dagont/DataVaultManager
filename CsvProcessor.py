import csv
import pandas as pd
import unidecode
import inflection
from Models.Column import Column, DataType
from Models import Model


class CsvProcessor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(CsvProcessor, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.file_path = None
        self.columns = []

    @staticmethod
    def detect_delimiter(file_path, sample_size=8192):
        with open(file_path, "r", newline='', encoding='utf-8') as csvfile:
            sample = csvfile.read(sample_size)
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                delimiter = dialect.delimiter
                return delimiter
            except csv.Error:
                # Fallback delimiter
                print("Delimiter identification failed")
                return ','

    def read_csv(self, file_path):
        if file_path:
            self.file_path = file_path
            delimiter = self.detect_delimiter(file_path)
            df = pd.read_csv(file_path, sep=delimiter)

        return df

    def extract_headers_and_data_types(self, df):
        headers = df.columns.tolist()
        data_types = []

        for col in df.columns:
            dt = df[col].dtype
            if dt == 'int64':
                dt = 'BIGINT'
            elif dt == 'float64':
                dt = 'DECIMAL'
            elif dt == 'datetime64[ns]':
                dt = 'DATETIME'
            elif dt == 'bool':
                dt = 'BIT'
            else:
                dt = 'NVARCHAR'
            data_types.append(DataType(dt))

        self.columns = [Column(h, False, dt, None) for h, dt in zip(headers, data_types)]

        return headers, data_types

    def extract_headers(self, df):
        headers = df.columns.tolist()
        self.columns = [Column(h, False, None, None) for h in headers]
        self.extract_data_types(df)
        return headers

    def extract_data_types(self, df):
        data_types = []
        for col in df.columns:
            dt = df[col].dtype
            if dt == 'int64':
                dt = 'BIGINT'
            elif dt == 'float64':
                dt = 'DECIMAL'
            elif dt == 'datetime64[ns]':
                dt = 'DATETIME'
            elif dt == 'bool':
                dt = 'BIT'
            else:
                dt = 'NVARCHAR'
            data_types.append(DataType(dt))

        # Update the data type in the Column instances
        for column, data_type in zip(self.columns, data_types):
            column.data_type = data_type

        return data_types

    def extract_business_names(self, headers):
        business_names = []
        for h in headers:
            cleaned_name = h.replace(' ', '_')  # replace spaces with underscores
            cleaned_name = unidecode.unidecode(cleaned_name)  # remove accents
            cleaned_name = inflection.titleize(cleaned_name)  # apply INITCAP
            cleaned_name = cleaned_name.replace(' ', '')  # remove spaces created by titleize
            business_names.append(cleaned_name)

        # Update the business name in the Column instances
        for column, business_name in zip(self.columns, business_names):
            column.business_name = business_name

        return business_names
