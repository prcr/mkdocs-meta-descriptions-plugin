from string import Template

from .common import logger


class Checker:
    """Checks meta descriptions against general SEO recommendations."""
    __initialized = False
    __check = False
    __min_length = 50
    __max_length = 160
    __template_warning_missing = Template(
        "Meta description not found: $page")
    __template_warning_length = Template(
        "Meta description $character_count character$plural $comparative than $limit: $page")

    def __check_length(self, page):
        length = len(page.meta.get("description", ""))
        if length == 0:
            logger.write(logger.Warning, self.__template_warning_missing.substitute(page=page.file.src_path))
            return  # Skip length check
        elif length < self.__min_length:
            diff = self.__min_length - length
            logger.write(logger.Warning, self.__template_warning_length.substitute(character_count=diff,
                                                                                   plural="s"[:diff != 1],
                                                                                   comparative="shorter",
                                                                                   limit=self.__min_length,
                                                                                   page=page.file.src_path))
        elif length > self.__max_length:
            diff = length - self.__max_length
            logger.write(logger.Warning, self.__template_warning_length.substitute(character_count=diff,
                                                                                   plural="s"[:diff != 1],
                                                                                   comparative="longer",
                                                                                   limit=self.__max_length,
                                                                                   page=page.file.src_path))

    def initialize(self, config):
        self.__check = config.get("enable_checks")
        self.__min_length = config.get("min_length")
        self.__max_length = config.get("max_length")
        self.__initialized = True

    def check(self, page):
        if not self.__initialized:
            logger.write(logger.Warning, "'LengthChecker' object not initialized yet, using default configurations")
        if self.__check:
            self.__check_length(page)


checker = Checker()
