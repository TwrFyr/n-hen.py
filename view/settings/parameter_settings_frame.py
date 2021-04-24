from tkinter import *
from typing import Optional

from util.view.tool_tip import CreateToolTip


class ParameterSettingsFrame(Frame):
    """
    Settings row for a basic setting.
    DO NOT CHANGE THIS. CHANGES ARE TO BE MADE TO `DirectorySettingsFrame`, since this is the same row without one button.
    """

    def __init__(self, **kw):
        super().__init__(**kw)

        row_padx = 5
        row_pady = 1
        title_max_length = 20

        self.label_name = Label(master=self, text='', width=title_max_length, anchor='w')
        self.label_name.grid(row=0, column=0, padx=row_padx, pady=row_pady)
        self.tooltip_label_name = CreateToolTip(widget=self.label_name, text=None)

        self.default_value = None
        self.entry_path_value = StringVar()
        self.entry_path = Entry(master=self, textvariable=self.entry_path_value)
        self.entry_path.grid(row=0, column=1, sticky='we', padx=row_padx, pady=row_pady)

        self.btn_reset = Button(master=self, text='Reset', command=self.onReset)
        self.btn_reset.grid(row=0, column=2, padx=row_padx, pady=row_pady)

        self.grid_columnconfigure(1, weight=1)

        self.validate_func = None

        self.activated = None
        self.setActivation(False)

    def setTitle(self, title: str):
        self.label_name.configure(text=title)

    def setTitleToolTip(self, tooltip: str):
        self.tooltip_label_name.text = tooltip

    def setValue(self, value: str):
        self.entry_path_value.set(value)
        self.entry_path.update_idletasks()

    def getValue(self) -> str:
        return self.entry_path_value.get()

    def setDefault(self, default: Optional[str]):
        self.default_value = default

    def checkValidation(self) -> bool:
        return self.validate_func is None or self.validate_func(self.entry_path_value.get())

    def validate(self):
        if self.checkValidation():
            print('valid')
        else:
            print('invalid')

    def setValidateFunc(self, func):
        self.validate_func = func

    def setActivation(self, activated: bool):
        if activated is not self.activated:
            if activated:
                self.entry_path.config(state=NORMAL)
                self.btn_reset.config(state=NORMAL)
            else:
                self.entry_path.config(state=DISABLED)
                self.btn_reset.config(state=DISABLED)
        self.activated = activated

    def onReset(self):
        if self.default_value is not None:
            self.setValue(self.default_value)
