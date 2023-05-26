import customtkinter as ctk
import tkinter as tk
from Controller import Controller
from Models.DataVaultEntity import DataVaultEntity

ctk.set_appearance_mode("dark")


class EntityDefinition(ctk.CTkFrame):
    CHECKBOX_WIDTH = 56
    DELETE_BUTTON_PADDING_X = (0, 50)

    def __init__(self, *args, label_text="Label", **kwargs):
        self.on_delete = kwargs.pop('on_delete', None)
        super().__init__(*args, **kwargs)
        self.label_text = label_text
        self.create_widgets()
        self.controller = Controller()

    def create_widgets(self):
        self.create_label()
        self.create_checkboxes()
        self.create_delete_button()

    def create_label(self):
        self.label = ctk.CTkLabel(master=self, text=self.label_text, width=230)
        self.label.pack(side="left", padx=(0, 3), anchor="w")

    def create_checkboxes(self):
        self.hub_checkbox = self.create_checkbox()
        self.sat_checkbox = self.create_checkbox()
        self.link_checkbox = self.create_checkbox()

    def create_checkbox(self):
        checkbox = ctk.CTkCheckBox(master=self, text="", width=self.CHECKBOX_WIDTH)
        checkbox.pack(side="left", padx=(0, 5))
        return checkbox

    def create_delete_button(self):
        delete_button = ctk.CTkButton(master=self, text="Delete", command=self.delete_element)
        delete_button.pack(side="left", padx=self.DELETE_BUTTON_PADDING_X)

    def delete_element(self):
        if self.on_delete is not None:
            self.on_delete(self)  # Call the callback before destroying
        self.destroy()

    def get_checkboxes(self):
        return [child for child in self.winfo_children() if isinstance(child, ctk.CTkCheckBox)]

    def to_data_vault_entity(self):
        return DataVaultEntity(
            name=self.label_text,
            is_hub=self.hub_checkbox.get(),
            is_sat=self.sat_checkbox.get(),
            is_link=self.link_checkbox.get()
        )


class FrameTwo(ctk.CTkFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.controller = Controller()
        self.entity_def_count = 0


        self.regular = ctk.CTkFont(family="Roboto", size=14)
        self.subtle = ctk.CTkFont(family="Roboto", size=12)

        self.title_label = ctk.CTkLabel(
            master=self, text="The suggested entities are", font=self.regular
        )
        self.title_label.pack(pady=(20, 10))

        self.row_desc = ctk.CTkLabel(
            master=self, text="Entity name\t          Hub            Sat             Link", font=self.regular
        )
        self.row_desc.pack(padx=(80, 10), pady=(20, 10), anchor="nw")

        self.scrollable_custom_frame = ctk.CTkScrollableFrame(self, width=580, height=200)
        self.scrollable_custom_frame.pack(pady=(0, 10), fill="both", expand=True)

        self.label_entry = ctk.CTkEntry(master=self, font=self.regular, width=230)
        self.label_entry.pack(pady=(0, 10))
        self.label_entry.bind("<Return>", self.add_new_entity_definition)

        self.add_new_btn = ctk.CTkButton(
            master=self, text="Add new", command=self.add_new_entity_definition, font=self.regular
        )
        self.add_new_btn.pack(pady=(0, 20))

        self.entity_definitions = []

    def get_data_vault_entities(self):
        print([type(entity_def.to_data_vault_entity()) for entity_def in self.entity_definitions])
        return [entity_def.to_data_vault_entity() for entity_def in self.entity_definitions]

    def process_data(self):
        entities = self.get_data_vault_entities()
        self.controller.process_data("FrameTwo", entities=entities)
        self.app.create_frame_four_instances(self.entity_def_count, self.controller.get_entities())


        #self.master.show_frame(GUI_FrameThree.FrameThree)

    def add_new_entity_definition(self, event=None):
        label_text = self.label_entry.get()
        self.label_entry.delete(0, tk.END)
        entity_def = EntityDefinition(self.scrollable_custom_frame, label_text=label_text, on_delete=self.remove_entity_definition)
        entity_def.pack(pady=(0, 5), fill="x")
        self.entity_definitions.append(entity_def)
        self.entity_def_count += 1

    def get_entity_definitions(self):
        return self.entity_definitions

    def remove_entity_definition(self, entity_def):
        if entity_def in self.entity_definitions:
            self.entity_definitions.remove(entity_def)
            self.entity_def_count -= 1


