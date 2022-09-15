import tkinter as tk
from tkinter import ttk


class VehicleTrimForm(tk.Frame):
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.inputs = {}
        # Labels
        self.vehiclemake_label = ttk.Label(self, text=fields['vehiclemake']['label'])
        self.vehiclemodel_label = ttk.Label(self, text=fields['vehiclemodel']['label'])
        self.vehicletrim_name_label = ttk.Label(self, text=fields['name']['label'])
        # Lookups and inputs
        self.vehiclemake_lookups = fields['vehiclemake']['values']
        self.inputs['vehiclemake'] = ttk.Combobox(
            self, values=['', *self.vehiclemake_lookups]
        )
        self.vehiclemodel_lookups = fields['vehiclemodel']['values']
        self.inputs['vehiclemodel'] = ttk.Combobox(
            self, values=['', *self.vehiclemodel_lookups]
        )
        self.vehicletrim_name_var = tk.StringVar()
        self.inputs['name'] = ttk.Entry(self, textvariable=self.vehicletrim_name_var)
        # Buttons to open new forms
        self.vehiclemake_form_btn = ttk.Button(self, text='Add VehicleMake')
        self.vehiclemodel_form_btn = ttk.Button(self, text='Add VehicleModel')
        # A save button
        self.save_btn = ttk.Button(self, text='Save')
        # Layout
        self.vehiclemake_label.grid(column=0, row=0)
        self.vehiclemodel_label.grid(column=1, row=0)
        self.vehicletrim_name_label.grid(column=2, row=0)
        self.inputs['vehiclemake'].grid(column=0, row=1)
        self.inputs['vehiclemodel'].grid(column=1, row=1)
        self.inputs['name'].grid(column=2, row=1)
        self.vehiclemake_form_btn.grid(column=0, row=2)
        self.vehiclemodel_form_btn.grid(column=1, row=2)
        self.save_btn.grid(column=2, row=3)
