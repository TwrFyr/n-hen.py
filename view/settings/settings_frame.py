from tkinter import *
from view import view_constants as vc
from view.settings.directory_settings_frame import DirectorySettingsFrame
from view.settings.parameter_models import SettingsParameters, DirectoryPaths, exportToFile, importFromFile, \
    getDefaultSettings
from view.settings.parameter_settings_frame import IntParameterSettingsFrame, FloatParameterSettingsFrame


class SettingsFrame(Frame):
    """
    A frame containing the `settings` part of the application.
    """

    def __init__(self, **kw):
        super().__init__(**kw)

        label_headline = Label(master=self, text='Settings', font=vc.HEADER_FONT)
        label_headline.pack()

        # setting entries
        settings_display_frame = Frame(master=self)
        settings_display_frame.pack(fill=X)

        default_settings = getDefaultSettings()

        self.saved_settings = None

        self.__validatable_settings_list = []

        self.download_directory = DirectorySettingsFrame(master=settings_display_frame)
        self.download_directory.setTitle('download directory')
        self.download_directory.setTitleToolTip('The directory in which individually downloaded doujins are saved.')
        self.download_directory.setDefault(default_settings.directory_paths.downloads)
        self.download_directory.pack(fill=X, expand=1)
        self.__validatable_settings_list.append(self.download_directory)

        self.favorites_directory = DirectorySettingsFrame(master=settings_display_frame)
        self.favorites_directory.setTitle('favorites directory')
        self.favorites_directory.setTitleToolTip('The directory in which all downloaded favourited doujins are saved.')
        self.favorites_directory.setDefault(default_settings.directory_paths.favorites)
        self.favorites_directory.pack(fill=X, expand=1)
        self.__validatable_settings_list.append(self.favorites_directory)

        self.thread_count = IntParameterSettingsFrame(master=settings_display_frame)
        self.thread_count.setTitle('thread count')
        self.thread_count.setTitleToolTip(
            'The number of concurrent connections when downloading.\nSetting it higher than the maximum number of CPU threads does not increase download speed further.')
        self.thread_count.setDefault(default_settings.thread_count)
        self.thread_count.setBounds(1, getDefaultSettings().thread_count * 2)
        self.thread_count.pack(fill=X, expand=1)
        self.__validatable_settings_list.append(self.thread_count)

        self.favorite_download_timeout = FloatParameterSettingsFrame(master=settings_display_frame)
        self.favorite_download_timeout.setTitle('download timeout')
        self.favorite_download_timeout.setTitleToolTip(
            'The time waited between downloading favorite entries in seconds.')
        self.favorite_download_timeout.setDefault(default_settings.download_delay)
        self.favorite_download_timeout.setBounds(1.0, 30.0)
        self.favorite_download_timeout.pack(fill=X, expand=1)
        self.__validatable_settings_list.append(self.favorite_download_timeout)

        for frame in self.__validatable_settings_list:
            frame.validate_callback = self.validateAllSettings

        # control buttons
        self.buttons_frame = Frame(master=self)
        self.buttons_frame.pack()

        self.isEditing = False
        self.btn_reset = Button(master=self.buttons_frame, text='Reset All', command=lambda: onResetAll(self))

        self.btn_edit = Button(master=self.buttons_frame, text='Edit', command=lambda: onEdit(self))
        self.btn_edit.grid(row=0, column=1)

        self.btn_apply = Button(master=self.buttons_frame, text='Apply', command=lambda: onApply(self))

    def toggleBtnApply(self, visible: bool):
        if visible:
            self.btn_apply.grid(row=0, column=2)
        else:
            self.btn_apply.grid_forget()

    def toggleBtnResetAll(self, visible: bool):
        if visible:
            self.btn_reset.grid(row=0, column=0)
        else:
            self.btn_reset.grid_forget()

    def setEditable(self, editable: bool):
        self.download_directory.setActivation(editable)
        self.favorites_directory.setActivation(editable)
        self.thread_count.setActivation(editable)
        self.favorite_download_timeout.setActivation(editable)
        self.focus()

    def onDisplay(self):
        settings = importFromFile('settings.json')
        if settings is None:
            print('no settings found -> resorting to default settings')
            settings = getDefaultSettings()
        _setCurrentSettings(self, settings)

    def onHide(self):
        pass

    def checkValidation(self):
        for frame in self.__validatable_settings_list:
            if not frame.checkValidation():
                return False
        return True

    def validateAllSettings(self):
        if self.checkValidation():
            self.btn_apply.configure(state=NORMAL)
        else:
            self.btn_apply.configure(state=DISABLED)


def onResetAll(settings_frame: SettingsFrame):
    print('reset')
    _setCurrentSettings(settings_frame, getDefaultSettings())


def onEdit(settings_frame: SettingsFrame):
    if settings_frame.isEditing:
        print('cancel')
        settings_frame.btn_edit.configure(text='Edit')
        settings_frame.toggleBtnApply(False)
        settings_frame.toggleBtnResetAll(False)
        settings_frame.setEditable(False)
        _setCurrentSettings(settings_frame, settings_frame.saved_settings)
        settings_frame.saved_settings = None
    else:
        print('edit')
        settings_frame.saved_settings = _getCurrentSettings(settings_frame)
        settings_frame.btn_edit.configure(text='Cancel')
        settings_frame.toggleBtnApply(True)
        settings_frame.toggleBtnResetAll(True)
        settings_frame.setEditable(True)
    settings_frame.isEditing = not settings_frame.isEditing


def onApply(settings_frame: SettingsFrame):
    print('apply')
    settings_frame.btn_edit.configure(text='Edit')
    settings_frame.toggleBtnApply(False)
    settings_frame.toggleBtnResetAll(False)
    settings_frame.setEditable(False)
    settings_frame.isEditing = not settings_frame.isEditing
    exportToFile(_getCurrentSettings(settings_frame), 'settings.json')
    settings_frame.saved_settings = None


def _getCurrentSettings(settings_frame: SettingsFrame) -> SettingsParameters:
    directories = DirectoryPaths(
        downloads=settings_frame.download_directory.getValue(),
        favorites=settings_frame.favorites_directory.getValue())
    return SettingsParameters(
        thread_count=settings_frame.thread_count.getValue(),
        download_delay=settings_frame.favorite_download_timeout.getValue(),
        directory_paths=directories)


def _setCurrentSettings(settings_frame: SettingsFrame, parameters: SettingsParameters):
    settings_frame.download_directory.setValue(parameters.directory_paths.downloads)
    settings_frame.favorites_directory.setValue(parameters.directory_paths.favorites)
    settings_frame.thread_count.setValue(parameters.thread_count)
    settings_frame.favorite_download_timeout.setValue(parameters.download_delay)
