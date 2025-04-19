import re
from textwrap import shorten
from html import escape

from bs4 import BeautifulSoup
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from .common import logger
from .export import Export
from .checker import checker


class MetaDescription(BasePlugin):

    config_scheme = (
        ("export_csv", config_options.Type(bool, default=False)),
        ("quiet", config_options.Type(bool, default=False)),
        ("enable_checks", config_options.Type(bool, default=False)),
        ("min_length", config_options.Type(int, default=50)),
        ("max_length", config_options.Type(int, default=160)),
        ("trim", config_options.Type(bool, default=False)),
        ("fallback_if_short", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        self.__headings_pattern = re.compile("<h[2-6]", flags=re.IGNORECASE)
        self.__pages = []
        self.__count_meta = 0             # Pages with meta descriptions defined on the page meta-data
        self.__count_first_paragraph = 0  # Pages with meta descriptions from the first paragraph
        self.__count_empty = 0            # Pages without meta descriptions

    def __get_first_paragraph_text(self, html):
        # Strip page subsections to improve performance
        html = re.split(self.__headings_pattern, html, maxsplit=1)[0]
        # Select first paragraph directly under body
        first_paragraph = BeautifulSoup(html, "html.parser").select_one("p:not(div.admonition > p)")
        if first_paragraph is not None:
            # Found the first paragraph, return stripped and escaped text
            return escape(first_paragraph.get_text().strip())
        else:
            # Didn't find the first paragraph
            return ""

    def on_config(self, config):
        logger.initialize(self.config)
        checker.initialize(self.config)
        return config

    def on_page_content(self, html, page, config, files):
        if page.meta.get("description", None):
            # Skip pages that already have an explicit meta description
            self.__count_meta += 1
            logger.write(logger.Debug, f"Adding meta description from front matter: {page.file.src_path}")
        else:
            # Create meta description based on the first paragraph of the page
            first_paragraph_text = self.__get_first_paragraph_text(html)
            if len(first_paragraph_text) == 0:
                self.__count_empty += 1
                logger.write(logger.Debug, f"Couldn't add meta description: {page.file.src_path}")
            elif (len(first_paragraph_text) < self.config.get("min_length")) & self.config.get("fallback_if_short"):
                self.__count_empty += 1
                logger.write(logger.Debug,
                             f"First paragraph is too short, reverting to site_description: {page.file.src_path}")
            else:
                if self.config.get("trim"):
                    page.meta["description"] = shorten(first_paragraph_text, self.config.get("max_length"),
                                                       placeholder="")
                else:
                    page.meta["description"] = first_paragraph_text
                self.__count_first_paragraph += 1
                logger.write(logger.Debug, f"Adding meta description from first paragraph: {page.file.src_path}")
        return html

    def on_post_page(self, output, page, config):
        if self.config.get("export_csv"):
            # Collect pages to export meta descriptions to CSV file
            self.__pages.append(page)
        checker.check(page)
        return output

    def on_post_build(self, config):
        count_meta = self.__count_meta + self.__count_first_paragraph
        count_total = count_meta + self.__count_empty
        logger.write(logger.Info, f"Added meta descriptions to {count_meta} of {count_total} pages, "
                                  f"{self.__count_first_paragraph} using the first paragraph")
        if self.config.get("export_csv"):
            # Export meta descriptions to CSV file
            Export(self.__pages, config).write_csv()
