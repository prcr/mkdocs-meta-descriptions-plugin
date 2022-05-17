import logging


class Logger:
    _tag = "[meta-descriptions] "
    _logger = logging.getLogger("mkdocs.mkdocs_meta_descriptions_plugin")

    Debug, Info, Warning, Error = range(0, 4)

    def write(self, log_level, message):
        message = self._tag + message
        if log_level == self.Debug:
            self._logger.debug(message)
        if log_level == self.Info:
            self._logger.info(message)
        if log_level == self.Warning:
            self._logger.warning(message)
        if log_level == self.Error:
            self._logger.error(message)


logger = Logger()
