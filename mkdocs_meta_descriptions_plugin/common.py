import logging

from mkdocs.plugins import BasePlugin


class Logger:
    Debug, Info, Warning, Error = range(0, 4)

    def __init__(self, verbose):
        self._tag = "[meta-descriptions] "
        self._logger = logging.getLogger("mkdocs.mkdocs_meta_descriptions_plugin")
        self._verbose = verbose

    def write(self, log_level, message):
        message = self._tag + message
        if log_level == self.Debug:
            self._logger.debug(message)
        elif log_level == self.Info:
            # Print info messages only if the verbose option is True
            if self._verbose:
                self._logger.info(message)
            else:
                self._logger.debug(message)
        elif log_level == self.Warning:
            self._logger.warning(message)
        elif log_level == self.Error:
            self._logger.error(message)


logger = Logger(BasePlugin.config.get("verbose", False))
