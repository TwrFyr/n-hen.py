""" tk_ToolTip_class101.py
gives a Tkinter widget a tooltip as the mouse is above the widget
tested with Python27 and Python34  by  vegaseat  09sep2014
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25mar16

Adjusted in https://stackoverflow.com/a/36221216.
"""

import tkinter as tk


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text=None, is_enabled=True):
        self.wait_time = 750  # miliseconds
        self.wrap_length = 300  # pixels
        self.widget = widget
        self.text = text
        self.is_enabled = is_enabled
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

        self.background_color = '#ffffff'

    def enter(self, event=None):
        if self.is_enabled and self.text is not None:
            self.schedule()

    def leave(self, event=None):
        if self.is_enabled and self.text is not None:
            self.unschedule()
            self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + self.widget.winfo_height()
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background=self.background_color, relief='solid', borderwidth=1,
                         wraplength=self.wrap_length)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
