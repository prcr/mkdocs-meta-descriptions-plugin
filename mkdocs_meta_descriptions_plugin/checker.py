from string import Template

from .common import logger


class Checker:
    """Checks meta descriptions against general SEO recommendations."""
    _initialized = False
    _check = False
    _min_length = 50
    _max_length = 160
    _warning_syntax_length = Template(
        "The meta description for $page is $character_count characters $comparative than $limit")

    def _check_length(self, page):
        length = len(page.meta.get("description", ""))
        if length == 0:
            # Skip length check
            # TODO Check that there's a warning for missing descriptions
            return
        elif length < self._min_length:
            diff = self._min_length - length
            logger.write(logger.Warning, self._warning_syntax_length.substitute(page=page.file.src_path,
                                                                                character_count=diff,
                                                                                comparative="shorter",
                                                                                limit=self._min_length))
        elif length > self._max_length:
            diff = length - self._max_length
            logger.write(logger.Warning, self._warning_syntax_length.substitute(page=page.file.src_path,
                                                                                character_count=diff,
                                                                                comparative="longer",
                                                                                limit=self._max_length))

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
