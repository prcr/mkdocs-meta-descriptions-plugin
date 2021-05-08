import os
import re
import logging
from urllib.parse import urlparse, unquote
import csv

from bs4 import BeautifulSoup
from usp.fetch_parse import XMLSitemapParser

PLUGIN_TAG = "[meta-descriptions] "
logger = logging.getLogger("mkdocs.mkdocs_meta_descriptions_plugin")


class Export:
    """Read meta descriptions from the generated HTML and export them as a CSV file."""

    def __init__(self, config, output_file="meta_descriptions.csv"):
        self._site_dir = config.get("site_dir")
        self._site_url = config.get("site_url")
        self._use_directory_urls = config.get("use_directory_urls")

        self._body_pattern = re.compile("<body", flags=re.IGNORECASE)
        self._output_path = os.path.join(self._site_dir, output_file)

        self._pages = None
        self._meta_descriptions = None
        if self._site_dir and self._site_url and self._output_path:
            self._pages = self._parse_sitemap()
            if self._pages:
                self._meta_descriptions = self._read_descriptions()

    def _parse_sitemap(self):
        sitemap_path = os.path.join(self._site_dir, "sitemap.xml")
        if not os.path.isfile(sitemap_path):
            logger.error(PLUGIN_TAG + f"Can't open sitemap {sitemap_path}")
            return None

        with open(sitemap_path) as sitemap_file:
            logger.info(PLUGIN_TAG + f"Reading {sitemap_path}")
            sitemap_content = sitemap_file.read()
            parser = XMLSitemapParser("", sitemap_content, 0, None)
        return parser.sitemap().pages

    def _read_descriptions(self):
        meta_descriptions = {}
        logger.info(PLUGIN_TAG + f"Reading meta descriptions from {len(self._pages)} HTML pages")
        count = 0
        for page in self._pages:
            # Transform URLs into local file names
            url_path = unquote(urlparse(page.url).path)[1:]
            page_path = os.path.join(self._site_dir, url_path)
            if self._use_directory_urls:
                page_path = os.path.join(page_path, "index.html")
            with open(page_path) as page_file:
                html = page_file.read()
                # Strip page body to improve performance
                html = re.split(self._body_pattern, html, maxsplit=1)[0]
                soup = BeautifulSoup(html, features="lxml")
                meta_element = soup.select_one("meta[name=\"description\"]")
                if meta_element:
                    count += 1
                    meta_descriptions[page_path] = meta_element.get("content")
                else:
                    meta_descriptions[page_path] = ""
        if count != len(self._pages):
            logger.warning(PLUGIN_TAG + f"Didn't find meta descriptions for {len(self._pages) - count} HTML pages")
        return meta_descriptions

    def write_csv(self):
        if self._meta_descriptions and self._meta_descriptions.keys():
            logger.info(PLUGIN_TAG + f"Writing {self._output_path}")
            with open(self._output_path, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Page", "Meta description"])
                for page, meta_description in self._meta_descriptions.items():
                    csv_writer.writerow([os.path.relpath(page, self._site_dir), meta_description])
        else:
            logger.error(PLUGIN_TAG + "Can't find meta descriptions to write to CSV file")
