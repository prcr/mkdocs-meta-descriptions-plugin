from logging import getLogger


class Logger:
    _initialized = False
    _tag = "[meta-descriptions] "
    _logger = getLogger("mkdocs.mkdocs_meta_descriptions_plugin")
    _quiet = False

    Debug, Info, Warning, Error = range(0, 4)

    def initialize(self, config):
        self._quiet = config.get("quiet")
        self._initialized = True

    def write(self, log_level, message):
        if not self._initialized:
            self._logger.warning(self._tag + "'Logger' object not initialized yet, using default configurations")

        message = self._tag + message
        if log_level == self.Debug:
            self._logger.debug(message)
        elif log_level == self.Info:
            # If quiet is True, print INFO messages as DEBUG
            if self._quiet:
                self._logger.debug(message)
            else:
                self._logger.info(message)
        elif log_level == self.Warning:
            self._logger.warning(message)
        elif log_level == self.Error:
            self._logger.error(message)


logger = Logger()
