from string import Template

from .common import logger


class Checker:
    """Checks meta descriptions against general SEO recommendations."""
    _initialized = False
    _check = False
    _min_length = 50
    _max_length = 160
    _template_warning_missing = Template(
        "Meta description not found: $page")
    _template_warning_length = Template(
        "Meta description $character_count character$plural $comparative than $limit: $page")

    def _check_length(self, page):
        length = len(page.meta.get("description", ""))
        if length == 0:
            logger.write(logger.Warning, self._template_warning_missing.substitute(page=page.file.src_path))
            return  # Skip length check
        elif length < self._min_length:
            diff = self._min_length - length
            logger.write(logger.Warning, self._template_warning_length.substitute(character_count=diff,
                                                                                  plural="s"[:diff != 1],
                                                                                  comparative="shorter",
                                                                                  limit=self._min_length,
                                                                                  page=page.file.src_path))
        elif length > self._max_length:
            diff = length - self._max_length
            logger.write(logger.Warning, self._template_warning_length.substitute(character_count=diff,
                                                                                  plural="s"[:diff != 1],
                                                                                  comparative="longer",
                                                                                  limit=self._max_length,
                                                                                  page=page.file.src_path))

    def initialize(self, config):
        self._check = config.get("enable_checks")
        self._min_length = config.get("min_length")
        self._max_length = config.get("max_length")
        self._initialized = True

    def check(self, page):
        if not self._initialized:
            logger.write(logger.Warning, "'LengthChecker' object not initialized yet, using default configurations")
        if self._check:
            self._check_length(page)


checker = Checker()
