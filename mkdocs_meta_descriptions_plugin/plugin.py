import re
import logging
from html import escape

from bs4 import BeautifulSoup

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

from .export import Export

PLUGIN_TAG = "[meta-descriptions] "
logger = logging.getLogger("mkdocs.mkdocs_meta_descriptions_plugin")


class MetaDescription(BasePlugin):

    config_scheme = (
        ("export_csv", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        self.headings_pattern = re.compile("<h[2-6]", flags=re.IGNORECASE)
        self.export_csv = False

    def get_first_paragraph_text(self, html):
        # Strip page subsections to improve performance
        html = re.split(self.headings_pattern, html, maxsplit=1)[0]
        # Select first paragraph directly under body
        first_paragraph = BeautifulSoup(html, features="lxml").select_one("body > p")
        if first_paragraph is not None:
            first_paragraph_text = first_paragraph.get_text().strip()
            first_paragraph_text = escape(first_paragraph_text)
            return first_paragraph_text
        else:
            return ""

    def on_page_content(self, html, page, config, files):
        if page.meta.get("description"):
            # Skip pages that already have an explicit meta description
            pass
        else:
            # Create description based on the first paragraph
            first_paragraph_text = self.get_first_paragraph_text(html)
            if len(first_paragraph_text) > 0:
                page.meta["description"] = first_paragraph_text
        return html

    def on_post_build(self, config):
        if self.config.get("export_csv", False):
            # Export meta descriptions to CSV file
            if not config.get("site_url"):
                logger.warning(PLUGIN_TAG + "Can't export meta descriptions to CSV because site_url is not defined.")
                return
            export = Export(config)
            export.write_csv()
