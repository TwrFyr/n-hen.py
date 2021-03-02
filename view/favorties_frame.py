from tkinter import *
from view import view_constants as vc
from view.favorite_entry_frame import FavoriteEntryFrame


class FavoritesFrame(Frame):

    def __init__(self, **kw):
        super().__init__(**kw)

        # --
        self.session_id = ''
        self.favorites = []
        # --

        label_headline = Label(master=self, text='Favorites', font=vc.HEADER_FONT)
        label_headline.pack()

        # --
        login_frame = Frame(master=self)
        login_frame.pack(fill=X)

        label_session_id = Label(master=login_frame, text='sessionId', font=vc.LABEL_FONT)
        label_session_id.grid(row=0, column=0, ipadx=10)

        self.entry_session_id = Entry(master=login_frame)
        self.entry_session_id.grid(row=0, column=1, sticky='ew')

        self.button_session_id = Button(master=login_frame, text='Load', font=vc.TEXT_FONT)
        self.button_session_id.grid(row=0, column=2)

        login_frame.columnconfigure(1, weight=1)
        # --

        # --
        favorites_list_frame = Frame(master=self, height=350, relief=SUNKEN, bd=2, padx=2, pady=2)
        favorites_list_frame.pack(fill=X)
        favorites_list_frame.pack_propagate(0)

        self.favorites_scroll_canvas = Canvas(master=favorites_list_frame)
        self.favorites_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.favorites_scrollbar = Scrollbar(master=favorites_list_frame, orient=VERTICAL, command=self.favorites_scroll_canvas.yview)
        self.favorites_scrollbar.pack(side=RIGHT, fill=Y)

        self.favorites_scroll_frame = Frame(master=self.favorites_scroll_canvas)
        self.favorites_scroll_frame.bind(
            "<Configure>",
            lambda e: self.favorites_scroll_canvas.configure(
                scrollregion=self.favorites_scroll_canvas.bbox("all")
            )
        )

        self.favorites_scroll_canvas.create_window((0, 0), window=self.favorites_scroll_frame, anchor='nw')
        self.favorites_scroll_canvas.configure(yscrollcommand=self.favorites_scrollbar.set)

        for i in range(0, 30):
            self.addItemToScrollList(i)
        # --

        # --
        directory_frame = Frame(master=self)
        directory_frame.pack(fill=X)

        self.entry_directory = Entry(master=directory_frame)
        self.entry_directory.grid(row=0, column=0, sticky='ew')

        self.button_directory = Button(master=directory_frame, text='Choose', font=vc.TEXT_FONT)
        self.button_directory.grid(row=0, column=1)

        directory_frame.columnconfigure(0, weight=1)
        # --

        # --
        download_status_frame = Frame(master=self)
        download_status_frame.pack(fill=X)

        self.button_download = Button(master=download_status_frame, text='Download', font=vc.TEXT_FONT)
        self.button_download.pack()

        self.label_entry_progress = Label(master=download_status_frame, text='3/26', font=vc.LABEL_FONT)
        self.label_entry_progress.pack()

        self.label_entry_in_progress = Label(master=download_status_frame, text='144725 - "Nekopara 01"',
                                             font=vc.TEXT_FONT)
        self.label_entry_in_progress.pack()

        self.label_page_progress = Label(master=download_status_frame, text='4/21', font=vc.TEXT_FONT)
        self.label_page_progress.pack()
        # --

    def setSessionIdButtonCommand(self, command):
        self.button_session_id.configure(command=command)

    def setDirectoryCommand(self, command):
        self.button_directory.configure(command=command)

    def addItemToScrollList(self, num):
        frame = FavoriteEntryFrame(master=self.favorites_scroll_frame, digits=num, name='Nekopara 01')
        frame.pack(fill=X)