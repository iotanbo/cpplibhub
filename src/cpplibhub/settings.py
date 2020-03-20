
"""
Read/write cpplibhub settings into the file, reset to default settings
"""

import configparser
# import logging
import sys

from iotanbo_py_utils import file_utils


class Settings:
    # This section contains some hardcoded and default settings
    DEFAULT_SETTINGS = {
        "PATHS": {
            "libhub_root": ""
        }
    }
    HOME_DIR = file_utils.get_user_home_dir() + "/.cpplibhub"
    PROJECT_LOGGER_FILE = HOME_DIR + "/cpplibhub.log"
    SETTINGS_FILE = HOME_DIR + "/cpplibhub.ini"

    parser = configparser.ConfigParser()

    print(f"* HOME_DIR: {HOME_DIR}")
    print(f"* PROJECT_LOGGER_FILE: {PROJECT_LOGGER_FILE}")
    print(f"* SETTINGS_FILE: {SETTINGS_FILE}")

    @classmethod
    def _init_home_dir(cls, delete_old: bool = False) -> None:
        """
        Called on new installation or if directory for some reason does not exist
        """

        # No logging here: logger may have not been initialized

        if file_utils.dir_exists(cls.HOME_DIR):
            if not delete_old:
                return
            else:
                file_utils.remove_dir_noexcept(cls.HOME_DIR)
        if file_utils.create_path_noexcept(cls.HOME_DIR)["error"]:
            print(f"Critical error: can't create home directory {cls.HOME_DIR}")
            sys.exit(-1)

        cls.create_default_settings()
        # TODO: create dir structure

    @classmethod
    def create_default_settings(cls, silent=True):
        # No logging here: logger may have not been initialized

        # Warn about .ini file recreated
        if not silent:
            print(f"Warning: old file '{cls.SETTINGS_FILE}' not found, creating new default settings.")

        # Create the file
        if file_utils.write_text_file_noexcept(cls.SETTINGS_FILE, "")["error"]:
            print(f"Critical error: can't write settings file: {cls.SETTINGS_FILE}")
            sys.exit(-1)

        # Set default values in the config parser
        cls.parser.read_dict(cls.DEFAULT_SETTINGS)

        # Write settings to file
        with open(cls.SETTINGS_FILE, 'w') as settings_file:
            cls.parser.write(settings_file)

    @classmethod
    def check_home_dir_integrity(cls) -> bool:
        """
        :return: True if success, False if problems found
        """
        if not file_utils.dir_exists(cls.HOME_DIR):
            cls._init_home_dir()
            return True
        if not file_utils.file_exists(cls.SETTINGS_FILE):
            cls.create_default_settings(silent=False)

    @classmethod
    def load(cls) -> bool:
        """
        Load settings from .ini file.
        """
        if not file_utils.file_exists(cls.SETTINGS_FILE):
            cls.create_default_settings(silent=False)

        # with open(cls.SETTINGS_FILE, 'r') as settings_file:
        #    cls.parser.read(settings_file, encoding="UTF-8")
        cls.parser.read(cls.SETTINGS_FILE)
        return True
