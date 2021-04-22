from time import sleep
from tkinter import *
from typing import Optional

from view import view_constants as vc
from view.favorite_entry_frame import FavoriteEntryFrame
from util import n_util
import os
from tkinter import filedialog
from util import dir_util
from util import n_download_util
import threading


class FavoritesFrame(Frame):

    def __init__(self, **kw):
        super().__init__(**kw)

        # -- model --
        self.n_user: Optional[n_util.NUser] = None
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
        user_info_frame = Frame(master=self)
        user_info_frame.pack(fill=X, padx=10, pady=10)

        pad_x = 10

        user_name_label = Label(master=user_info_frame, text='Username', font=vc.LABEL_FONT)
        user_name_label.grid(row=0, column=0, sticky=W)
        self.username_label_value = Label(master=user_info_frame, text='', font=vc.TEXT_FONT)
        self.username_label_value.grid(row=0, column=1, sticky=W, padx=pad_x)

        user_fav_count = Label(master=user_info_frame, text='Favorites count', font=vc.LABEL_FONT)
        user_fav_count.grid(row=1, column=0, sticky=W)
        self.user_fav_count_value = Label(master=user_info_frame, text='', font=vc.TEXT_FONT)
        self.user_fav_count_value.grid(row=1, column=1, sticky=W, padx=pad_x)

        user_info_frame.columnconfigure(1, weight=1)
        # --

        # --
        favorites_list_frame = Frame(master=self, height=350, relief=SUNKEN, bd=2, padx=2, pady=2)
        favorites_list_frame.pack(fill=X)
        favorites_list_frame.pack_propagate(0)

        self.favorites_scroll_canvas = Canvas(master=favorites_list_frame)
        self.favorites_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.favorites_scrollbar = Scrollbar(master=favorites_list_frame, orient=VERTICAL,
                                             command=self.favorites_scroll_canvas.yview)
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
        # --

        # --
        directory_frame = Frame(master=self)
        directory_frame.pack(fill=X)

        self.entry_directory_value = StringVar()
        self.entry_directory_value.set(os.path.join(os.getcwd(), 'favorites'))

        self.entry_directory = Entry(master=directory_frame, state=DISABLED, textvariable=self.entry_directory_value)
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

        self.label_entry_progress = Label(master=download_status_frame, text='', font=vc.LABEL_FONT)
        self.label_entry_progress.pack()

        self.label_entry_in_progress = Label(master=download_status_frame, text='',
                                             font=vc.TEXT_FONT)
        self.label_entry_in_progress.pack()

        self.label_page_progress = Label(master=download_status_frame, text='', font=vc.TEXT_FONT)
        self.label_page_progress.pack()
        # --

        self.setSessionIdButtonCommand(lambda: onLoad(self))
        self.setDirectoryCommand(lambda: onChoose(self))
        self.setDownloadCommand(lambda: onDownload(self))

    def setSessionIdButtonCommand(self, command):
        self.button_session_id.configure(command=command)

    def setDirectoryCommand(self, command):
        self.button_directory.configure(command=command)

    def setDownloadCommand(self, command):
        self.button_download.configure(command=command)

    def addItemToScrollList(self, digits: str, name: str):
        frame = FavoriteEntryFrame(master=self.favorites_scroll_frame, digits=digits, name=name)
        frame.pack(fill=X)

    def updateView(self):
        if self.n_user is None:
            for child in self.favorites_scroll_frame.winfo_children():
                child.destroy()
        else:
            self.username_label_value.configure(text=self.n_user.username)
            self.user_fav_count_value.configure(text=self.n_user.fav_count)
            for min_entry in self.n_user.favorite_list:
                self.addItemToScrollList(digits=min_entry.n_id, name=min_entry.name)

    def updateEntryProgress(self, current_entry: n_util.MinimizedNEntry, current: int, total: int):
        if current <= total and current_entry is not None:
            setAndUpdateLabelText(self.label_entry_progress, f'{current} / {total}')
            setAndUpdateLabelText(self.label_entry_in_progress, f'{current_entry.n_id} - "{current_entry.name}"')
        else:
            sleep(1)
            setAndUpdateLabelText(self.label_entry_progress, '')
            setAndUpdateLabelText(self.label_entry_in_progress, '')
            setAndUpdateLabelText(self.label_page_progress, '')

    def updatePageProgress(self, current, total):
        if current <= total:
            setAndUpdateLabelText(self.label_page_progress, f'{current} / {total}')
            if current == total:
                sleep(0.5)
                setAndUpdateLabelText(self.label_page_progress, '')


def onLoad(favorites_frame: FavoritesFrame):
    session_id = favorites_frame.entry_session_id.get()
    if session_id is None or session_id == '':
        favorites_frame.n_user = None
        favorites_frame.updateView()
        print('no sessionId provided')
        return
    favorites_frame.n_user = n_util.get_n_user(session_id)
    if favorites_frame.n_user is None:
        print('invalid sessionId')
    favorites_frame.updateView()


def onChoose(favorites_frame: FavoritesFrame):
    dir_util.create_dir_if_not_exists(favorites_frame.entry_directory_value.get())
    filename = filedialog.askdirectory(initialdir=favorites_frame.entry_directory_value.get(), mustexist=True)
    if len(filename) != 0:
        favorites_frame.entry_directory_value.set(filename)


def onDownload(favorites_frame: FavoritesFrame):
    if favorites_frame.n_user is not None:
        t = threading.Thread(target=n_download_util.download_all_favorites, kwargs=dict(
            n_user=favorites_frame.n_user,
            base_dir=favorites_frame.entry_directory_value.get(),
            update_entry=favorites_frame.updateEntryProgress,
            update_page=favorites_frame.updatePageProgress,
            thread_count=16))
        t.start()
    else:
        print('no n_user found')


def setAndUpdateLabelText(label: Label, text: str):
    label.configure(text=text)
    label.update_idletasks()
