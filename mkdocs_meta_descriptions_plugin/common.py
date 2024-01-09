import mkdocs
from packaging import version

MKDOCS_VERSION = version.parse(mkdocs.__version__)
MKDOCS_1_5_0 = version.parse("1.5.0")

if MKDOCS_VERSION < MKDOCS_1_5_0:
    from logging import getLogger
else:
    from mkdocs.plugins import get_plugin_logger


class Logger:
    __initialized = False
    if MKDOCS_VERSION < MKDOCS_1_5_0:
        __tag = "[meta-descriptions] "
        __logger = getLogger("mkdocs.plugins." + __name__)
    else:
        __tag = ""
        __logger = get_plugin_logger("meta-descriptions")
    __quiet = False

    Debug, Info, Warning, Error = range(0, 4)

    def initialize(self, config):
        self.__quiet = config.get("quiet")
        self.__initialized = True

    def write(self, log_level, message):
        if not self.__initialized:
            self.__logger.warning(self.__tag + "'Logger' object not initialized yet, using default configurations")

        message = self.__tag + message
        if log_level == self.Debug:
            self.__logger.debug(message)
        elif log_level == self.Info:
            # If quiet is True, print INFO messages as DEBUG
            if self.__quiet:
                self.__logger.debug(message)
            else:
                self.__logger.info(message)
        elif log_level == self.Warning:
            self.__logger.warning(message)
        elif log_level == self.Error:
            self.__logger.error(message)


logger = Logger()
