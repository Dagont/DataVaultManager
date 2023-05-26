import customtkinter as tk
import tkinter as tki
from tkinter import filedialog
import pandas as pd
import numpy as np

tk.set_appearance_mode("dark")


class CustomCTkScrollableFrame(tk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.inner_frame = self


class LabelButtonScrollableFrame(CustomCTkScrollableFrame):
    def __init__(self, master, button_text, **kwargs):
        super().__init__(master, **kwargs)
        self.button_text = button_text
        self.row = 0

    def add_label_button(self, text, callback=None, combo=False):
        if combo:
            data_type, col_name = text.split(" - ")
            data_type_options = ["SMALLINT", "INT", "BIGINT", "DECIMAL(10, 4)", "DATETIME", "TIME", "BIT", "NVARCHAR(MAX)"]
            data_type_combo = tk.CTkComboBox(master=self.inner_frame, values=data_type_options)
            data_type_combo.set(data_type)
            data_type_combo.grid(row=self.row, column=0, padx=(10, 0), pady=5, sticky="w")
        else:
            label = tk.CTkLabel(master=self.inner_frame, text=text)
            label.grid(row=self.row, column=0, padx=(10, 0), pady=5, sticky="w")

        if combo:
            col_label = tk.CTkLabel(master=self.inner_frame, text=col_name)
            col_label.grid(row=self.row, column=1, padx=(10, 0), pady=5, sticky="w")

        button = tk.CTkButton(master=self.inner_frame, text=self.button_text, width=20, height=1, command=callback)
        button.grid(row=self.row, column=2 if combo else 1, padx=(0, 0), pady=5, sticky="e")

        self.row += 1





class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DataVault 2.0 Manager")
        self.minsize(600, 500)

        self.file_path = None

        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        rowid = 1
        self.load_file_label = tk.CTkLabel(master=self, text="Load file")
        self.load_file_label.grid(row=rowid, column=0, columnspan=1, padx=20, pady=(20, 20), sticky="ew")

        self.file_selector_btn = tk.CTkButton(master=self, text="Select CSV File", command=self.select_csv_file)
        self.file_selector_btn.grid(row=rowid, column=1, columnspan=1, padx=20, pady=(20, 20), sticky="ew")

        rowid += 1
        self.detected_columns_label = tk.CTkLabel(master=self, text="Detected Columns")
        self.detected_columns_label.grid(row=rowid, column=1, padx=20, sticky="ew")

        self.empty_table_label = tk.CTkLabel(master=self, text="List of entities")
        self.empty_table_label.grid(row=rowid, column=0, sticky="ew")



        rowid += 1
        self.detected_columns_table = LabelButtonScrollableFrame(master=self, button_text='+', width=300, height=200)
        self.detected_columns_table.grid(row=rowid, column=1, padx=20, sticky="nsew")

        self.entity_buttons_frame = CustomCTkScrollableFrame(master=self)
        self.entity_buttons_frame.grid(row=rowid, column=0, padx=20, sticky="nsew")

        self.transferred_labels_frame = LabelButtonScrollableFrame(master=self, button_text='-', width=300, height=200)
        self.transferred_labels_frame.grid(row=rowid, column=2, padx=20, sticky="nsew")

        rowid += 1
        self.input_field = tk.CTkEntry(master=self)
        self.input_field.grid(row=rowid, column=0, padx=20, pady=(20, 5), sticky="ew")

        rowid += 1
        self.add_to_table_btn = tk.CTkButton(master=self, text="Add to Table", command=self.add_to_table)
        self.add_to_table_btn.grid(row=rowid, column=0, padx=20, pady=(0, 20), sticky="ew")

    def select_csv_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.load_csv_columns()



    def load_csv_with_auto_percentage_detection(self, file_path):
        temp_df = pd.read_csv(file_path, sep=",", nrows=1000)  # Read a portion of the CSV to detect percentage columns
        percent_columns = []

        for col in temp_df.columns:
            if temp_df[col].apply(lambda x: isinstance(x, str) and '%' in x).any():
                percent_columns.append(col)

        converters = {col: lambda x: float(x.strip('%')) / 100 if isinstance(x, str) and '%' in x else x for col in
                      percent_columns}
        return pd.read_csv(file_path, sep=",", converters=converters)

    def load_csv_columns(self):
        df = self.load_csv_with_auto_percentage_detection(self.file_path)
        mapped_data_types = self.detect_and_map_data_types(df)

        def create_callback(col_name):
            return lambda: self.transfer_label_to_frame(
                self.detected_columns_table, self.transferred_labels_frame, f"{sql_dtype} - {col_name}"
            )

        for col_name, sql_dtype in mapped_data_types.items():
            self.detected_columns_table.add_label_button(
                f"{sql_dtype} - {col_name}",
                callback=create_callback(col_name),
                combo=True
            )

    def transfer_label_to_frame(self, source_frame, target_frame, text):
        source_frame.inner_frame.forget(text)
        target_frame.add_label_button(text, callback=lambda: self.transfer_label_to_frame(target_frame, source_frame, text))

    def add_to_table(self):
        input_text = self.input_field.get()
        if input_text:
            self.add_entity_button(input_text)
            self.input_field.delete(0, tk.END)

    def add_entity_button(self, entity_name):
        button = tk.CTkButton(
            master=self.entity_buttons_frame.inner_frame,
            text=entity_name,
            command=lambda: self.display_entity_columns(entity_name)
        )
        button.pack(padx=10, pady=5, fill="x")

    def display_entity_columns(self, entity_name):
        # You will need to implement this function according to your requirements,
        # for example, by fetching the list of columns associated with the entity_name
        # from a database, and then displaying them in a table to the right of the container.
        pass


    def map_dtype_to_sql_server(self, dtype):
        if np.issubdtype(dtype, np.integer):
            if np.issubdtype(dtype, np.int8) or np.issubdtype(dtype, np.int16):
                return "SMALLINT"
            elif np.issubdtype(dtype, np.int32):
                return "INT"
            else:
                return "BIGINT"
        elif np.issubdtype(dtype, np.floating):
            return "DECIMAL(10, 4)"
        elif np.issubdtype(dtype, np.datetime64):
            return "DATETIME"
        elif np.issubdtype(dtype, np.timedelta64):
            return "TIME"
        elif np.issubdtype(dtype, np.bool_):
            return "BIT"
        elif pd.api.types.is_string_dtype(dtype):
            return "NVARCHAR(MAX)"
        else:
            return "NVARCHAR(MAX)"

    def is_percentage_column(self, dtype):
        return dtype.name.startswith("percentage")

    def detect_and_map_data_types(self, df):
        mapped_data_types = {}
        for col_name, dtype in df.dtypes.items():
            if pd.api.types.is_float_dtype(dtype) and df[col_name].apply(lambda x: 0 <= x <= 1).all():
                mapped_data_types[col_name] = "DECIMAL(10, 4)"
            else:
                mapped_data_types[col_name] = self.map_dtype_to_sql_server(dtype)
        return mapped_data_types




if __name__ == "__main__":
    app = App()
    app.mainloop()
