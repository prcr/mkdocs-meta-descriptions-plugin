import csv
import os
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .common import logger


class Export:
    """Read meta descriptions from the generated HTML and export them in a CSV file."""

    def __init__(self, pages, config):
        self._body_pattern = re.compile("<body", flags=re.IGNORECASE)
        self._site_dir = config.get("site_dir")
        self._site_url = config.get("site_url")
        self._meta_descriptions = self._read_meta_descriptions(pages)

    def _read_meta_descriptions(self, pages):
        count_missing = 0
        meta_descriptions = {}
        # Get meta descriptions only for Markdown documentation pages
        for page in filter(lambda p: p.file.is_documentation_page(), pages):
            with open(page.file.abs_dest_path) as page_file:
                html = page_file.read()
                # Strip page body to improve performance
                html = re.split(self._body_pattern, html, maxsplit=1)[0]
                soup = BeautifulSoup(html, "html.parser")
                meta_tag = soup.select_one('meta[name="description"]')
                if meta_tag:
                    meta_descriptions[page.url] = meta_tag.get("content")
                else:
                    count_missing += 1
                    meta_descriptions[page.url] = ""
        if count_missing > 0:
            logger.write(logger.Warning, f"Couldn't find meta descriptions for {count_missing} HTML pages")
        return meta_descriptions

    def write_csv(self, output_file="meta-descriptions.csv"):
        output_file_path = os.path.join(self._site_dir, output_file)
        if self._meta_descriptions:
            with open(output_file_path, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Page", "Meta description"])
                for url_path, meta_description in self._meta_descriptions.items():
                    csv_writer.writerow(
                        [urljoin(self._site_url, url_path), meta_description]
                    )
            logger.write(logger.Info, f"Exported meta descriptions to: {output_file_path}")
        else:
            logger.write(logger.Warning, "Can't find meta descriptions to write to CSV file")
