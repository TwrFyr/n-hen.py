from tkinter import *
from typing import Optional

from util.view.tool_tip import CreateToolTip
import view.view_constants as view_c


class StringParameterSettingsFrame(Frame):
    """
    Settings row for a basic setting.
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

        self.entry_value = StringVar()
        self.entry_value.trace("w", lambda *args: self.validate())
        self.entry = Entry(master=self, textvariable=self.entry_value)
        self.entry.grid(row=0, column=1, sticky='we', padx=row_padx, pady=row_pady)

        self.tooltip_entry = CreateToolTip(widget=self.entry, text=None, is_enabled=False)
        self.tooltip_entry.wrap_length = 400
        self.tooltip_entry.background_color = view_c.COLOR_ERROR

        self.btn_reset = Button(master=self, text='Reset', command=self.onReset)
        self.btn_reset.grid(row=0, column=2, padx=row_padx, pady=row_pady)

        self.grid_columnconfigure(1, weight=1)

        self.activated = None
        self.setActivation(False)

        self.__previous_is_valid = False
        self.validate_callback = None

    def setTitle(self, title: str):
        self.label_name.configure(text=title)

    def setTitleToolTip(self, tooltip: str):
        self.tooltip_label_name.text = tooltip

    def setInvalidToolTip(self, tooltip: str):
        self.tooltip_entry.text = tooltip

    def setValue(self, value: str):
        self.entry_value.set(value)
        self.entry.update_idletasks()

    def getValue(self) -> str:
        return self.entry_value.get()

    def setDefault(self, default: Optional[str]):
        self.default_value = default

    def checkValidation(self) -> bool:
        return True

    def validate(self):
        is_valid = self.checkValidation()
        if is_valid:
            self.entry.configure(background='white')
        else:
            self.entry.configure(background=view_c.COLOR_ERROR)
        self.tooltip_entry.is_enabled = not is_valid

        if (is_valid is not self.__previous_is_valid) and self.validate_callback is not None:
            self.validate_callback()
        self.__previous_is_valid = is_valid

    def setActivation(self, activated: bool):
        if activated is not self.activated:
            if activated:
                self.entry.config(state=NORMAL)
                self.btn_reset.config(state=NORMAL)
            else:
                self.entry.config(state=DISABLED)
                self.btn_reset.config(state=DISABLED)
        self.activated = activated

    def onReset(self):
        if self.default_value is not None:
            self.setValue(self.default_value)


class IntParameterSettingsFrame(StringParameterSettingsFrame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bound_lower = None
        self.bound_upper = None

        self.tooltip_entry.text = self.__generateInvalidToolTip()

    # -- override

    def setValue(self, value: int):
        self.entry_value.set(str(value))
        self.entry.update_idletasks()

    def getValue(self) -> Optional[int]:
        if self.checkValidation():
            return int(self.entry_value.get())
        else:
            return None

    def setDefault(self, default: Optional[int]):
        self.default_value = default

    def checkValidation(self) -> bool:
        try:
            value = int(self.entry_value.get())
            return not ((self.bound_lower is not None and value < self.bound_lower) or (
                    self.bound_upper is not None and value > self.bound_upper))
        except ValueError:
            return False

    # -- new members

    def setBounds(self, bound_lower: Optional[int], bound_upper: Optional[int]):
        self.bound_lower = bound_lower
        self.bound_upper = bound_upper
        self.tooltip_entry.text = self.__generateInvalidToolTip()

    def __generateInvalidToolTip(self):
        tooltip = "Value must be a valid integer (e.g. '6', '-5', '+11')."
        if (self.bound_lower is not None) and (self.bound_upper is not None):
            tooltip += f"\nValue must be at least {self.bound_lower} and {self.bound_upper} at most."
        elif self.bound_lower is not None:
            tooltip += f"\nValue must be at least {self.bound_lower}."
        elif self.bound_upper is not None:
            tooltip += f"\nValue must be {self.bound_upper} at most."
        return tooltip


class FloatParameterSettingsFrame(StringParameterSettingsFrame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bound_lower = None
        self.bound_upper = None

        self.tooltip_entry.text = self.__generateInvalidToolTip()

    # -- override

    def setValue(self, value: float):
        self.entry_value.set(str(value))
        self.entry.update_idletasks()

    def getValue(self) -> Optional[float]:
        if self.checkValidation():
            return float(self.entry_value.get())
        else:
            return None

    def setDefault(self, default: Optional[float]):
        self.default_value = default

    def checkValidation(self) -> bool:
        try:
            value = float(self.entry_value.get())
            return not ((self.bound_lower is not None and (value < self.bound_lower)) or (
                    self.bound_upper is not None and value > self.bound_upper))
        except ValueError:
            return False

    # -- new members

    def setBounds(self, bound_lower: Optional[float], bound_upper: Optional[float]):
        self.bound_lower = bound_lower
        self.bound_upper = bound_upper
        self.tooltip_entry.text = self.__generateInvalidToolTip()

    def __generateInvalidToolTip(self):
        tooltip = "Value must be a valid decimal number (e.g. '6', '-5.4', '+11.842')."
        if (self.bound_lower is not None) and (self.bound_upper is not None):
            tooltip += f"\nValue must be at least {self.bound_lower} and {self.bound_upper} at most."
        elif self.bound_lower is not None:
            tooltip += f"\nValue must be at least {self.bound_lower}."
        elif self.bound_upper is not None:
            tooltip += f"\nValue must be {self.bound_upper} at most."
        return tooltip
