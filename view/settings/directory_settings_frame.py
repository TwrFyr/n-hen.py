from tkinter import *


class DirectorySettingsFrame(Frame):
    """
    A settings row for a directory path with a button to select a directory and a button to reset the setting.
    """

    def __init__(self, **kw):
        super().__init__(**kw)

        row_padx = 5
        row_pady = 1
        title_max_length = 20

        self.label_name = Label(master=self, text='', width=title_max_length, anchor='w')
        self.label_name.grid(row=0, column=0, padx=row_padx, pady=row_pady)

        self.entry_path_value = StringVar()
        self.entry_path = Entry(master=self)
        self.entry_path.grid(row=0, column=1, sticky='we', padx=row_padx, pady=row_pady)

        self.btn_choose = Button(master=self, text='Choose')
        self.btn_choose.grid(row=0, column=2, padx=row_padx, pady=row_pady)

        self.btn_reset = Button(master=self, text='Reset')
        self.btn_reset.grid(row=0, column=3, padx=row_padx, pady=row_pady)

        self.grid_columnconfigure(1, weight=1)

        self.validate_func = None

        self.activated = None
        self.setActivation(False)

    def setTitle(self, title: str):
        self.label_name.configure(text=title)

    def setValue(self, value: str):
        self.entry_path_value.set(value)

    def getValue(self) -> str:
        return self.entry_path_value.get()

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
                self.btn_choose.config(state=NORMAL)
                self.btn_reset.config(state=NORMAL)
            else:
                self.entry_path.config(state=DISABLED)
                self.btn_choose.config(state=DISABLED)
                self.btn_reset.config(state=DISABLED)
        self.activated = activated
