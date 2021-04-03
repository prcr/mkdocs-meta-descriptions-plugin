from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin


class MetaDescription(BasePlugin):

    config_scheme = (
        ('param', config_options.Type(str, default="")),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0


    def on_page_content(self, html, page, config, files):
        return html
