
"""
Read/write cpplibhub settings into the file
"""

import configparser


class CpplibhubSettings:

    DEFAULT_SETTINGS = {
        "PATHS": {
            "libhub": "/C/cpplibhub",
            "home": "~/cpplibhub"  # user settings and other data
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = configparser.ConfigParser()

    def load(self) -> None:
        """
        Load settings from `cpplibhub.ini`.
        This file must be located in ~/cpplibhub dir
        on unix-like systems.
        """
        # Set defaults
        for section, values in self.DEFAULT_SETTINGS.items():
            self.settings.set(section, values)
        # If settings file exists, load settings from file
