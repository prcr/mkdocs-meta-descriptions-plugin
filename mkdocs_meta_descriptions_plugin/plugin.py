import re

from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

from bs4 import BeautifulSoup


class MetaDescription(BasePlugin):

    config_scheme = (
        ('param', config_options.Type(str, default="")),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_page_content(self, html, page, config, files):
        if page.meta.get("description"):
            # Skip pages that have an explicit meta description
            pass
        else:
            # Create description based on the first paragraph
            first_paragraph = self.get_first_paragraph(html)
            if first_paragraph is not None and len(first_paragraph) > 0:
                page.meta["description"] = first_paragraph
        return html

    @staticmethod
    def get_first_paragraph(html):
        # Strip all page content in subsections
        html = re.split("<h[2-6]", html, maxsplit=1, flags=re.IGNORECASE)[0]
        # Obtain first paragraph that is direct child of body element
        first_paragraph = BeautifulSoup(html, features="lxml").select_one("body > p")
        if first_paragraph is not None:
            return first_paragraph.get_text()
        return None
