from dataclasses import dataclass, asdict
import json
import os
from typing import Optional


@dataclass
class DirectoryPaths:
    downloads: str
    favorites: str


@dataclass
class SettingsParameters:
    thread_count: int
    download_delay: float
    directory_paths: DirectoryPaths


def settingsToDict(settings_parameters: SettingsParameters) -> dict:
    return asdict(settings_parameters)


def dictToSettings(dictionary: dict) -> SettingsParameters:
    directory_paths = DirectoryPaths(
        downloads=dictionary['directory_paths']['downloads'],
        favorites=dictionary['directory_paths']['favorites'])
    return SettingsParameters(
        directory_paths=directory_paths,
        thread_count=dictionary['thread_count'],
        download_delay=dictionary['download_delay'])


def exportToFile(settings: SettingsParameters, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(settingsToDict(settings), f, indent=4)


def importFromFile(file_path: str) -> Optional[SettingsParameters]:
    """
    Returns the settings parameters saved in the given file. Returns None if opening the file results in an error.
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'r') as f:
            return dictToSettings(json.load(f))
    except OSError as err:
        print(err)
        return None


def getDefaultSettings() -> SettingsParameters:
    """
    Returns the `SettingsParameters` instance used for the default values.
    :return:
    """
    directories = DirectoryPaths(
        downloads='saves',
        favorites='favorites')
    cpu_count = len(os.sched_getaffinity(0))
    if cpu_count is None:
        cpu_count = 8
    return SettingsParameters(
        thread_count=cpu_count,
        download_delay=2.0,
        directory_paths=directories)
