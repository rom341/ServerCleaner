import configparser


class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.read(file_path, encoding="utf-8")

    def get(self, section, parameter, fallback=None):
        try:
            return self.config.get(section, parameter, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def get_int(self, section, parameter, fallback=None):
        try:
            return self.config.getint(section, parameter, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def get_float(self, section, parameter, fallback=None):
        try:
            return self.config.getfloat(section, parameter, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def get_boolean(self, section, parameter, fallback=None):
        try:
            return self.config.getboolean(section, parameter, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback

    def get_all_parameters(self, section):
        try:
            return dict(self.config.items(section))
        except configparser.NoSectionError:
            return {}

    def sections(self):
        return self.config.sections()
