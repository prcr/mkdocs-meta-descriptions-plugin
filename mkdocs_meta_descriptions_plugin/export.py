import os
import re
import csv

from bs4 import BeautifulSoup

from .common import logger, PLUGIN_TAG


class Export:
    """Read meta descriptions from the generated HTML and export them in a CSV file."""

    def __init__(self, pages, config):
        self._body_pattern = re.compile("<body", flags=re.IGNORECASE)
        self._site_dir = config.get("site_dir")
        self._meta_descriptions = self._read_meta_descriptions(pages)

    def _read_meta_descriptions(self, pages):
        logger.info(
            PLUGIN_TAG + f"Reading meta descriptions from {len(pages)} HTML pages"
        )
        count_missing = 0
        meta_descriptions = {}
        # Get meta descriptions only for Markdown documentation pages
        for page in filter(lambda p: p.file.is_documentation_page(), pages):
            with open(page.file.abs_dest_path) as page_file:
                html = page_file.read()
                # Strip page body to improve performance
                html = re.split(self._body_pattern, html, maxsplit=1)[0]
                soup = BeautifulSoup(html, features="lxml")
                meta_tag = soup.select_one('meta[name="description"]')
                if meta_tag:
                    meta_descriptions[page.file.dest_path] = meta_tag.get("content")
                else:
                    count_missing += 1
                    meta_descriptions[page.file.dest_path] = ""
        if count_missing > 0:
            logger.warning(
                PLUGIN_TAG
                + f"Couldn't find meta descriptions for {count_missing} HTML pages"
            )
        return meta_descriptions

    def write_csv(self, output_file="meta_descriptions.csv"):
        output_file_path = os.path.join(self._site_dir, output_file)
        if self._meta_descriptions:
            logger.info(PLUGIN_TAG + f"Writing {output_file_path}")
            with open(output_file_path, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Page", "Meta description"])
                for page_rel_path, meta_description in self._meta_descriptions.items():
                    csv_writer.writerow([page_rel_path, meta_description])
        else:
            logger.error(
                PLUGIN_TAG + "Can't find meta descriptions to write to CSV file"
            )
