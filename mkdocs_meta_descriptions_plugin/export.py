import os
import re
import logging
from urllib.parse import unquote
import csv

from bs4 import BeautifulSoup
from usp.fetch_parse import XMLSitemapParser

PLUGIN_TAG = "[meta-descriptions] "
logger = logging.getLogger("mkdocs.mkdocs_meta_descriptions_plugin")


class Export:
    def __init__(self, config, output_file="meta_descriptions.csv"):
        self.site_dir = config.get("site_dir")
        self.site_url = config.get("site_url")
        self.use_directory_urls = config.get("use_directory_urls")

        self.body_pattern = re.compile("<body", flags=re.IGNORECASE)
        self.output_path = os.path.join(self.site_dir, output_file)

        self.pages = None
        self.meta_descriptions = None
        if self.site_dir and self.site_url and self.output_path:
            self.pages = self._parse_sitemap()
            if self.pages:
                self.meta_descriptions = self._read_descriptions()

    def _parse_sitemap(self):
        sitemap_path = os.path.join(self.site_dir, "sitemap.xml")
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
        logger.info(PLUGIN_TAG + f"Reading meta descriptions from {len(self.pages)} HTML pages")
        count = 0
        for page in self.pages:
            # Transform URLs in local file names
            page_path = os.path.join(self.site_dir, unquote(page.url).replace(self.site_url, ""))
            if self.use_directory_urls:
                page_path = os.path.join(page_path, "index.html")
            with open(page_path) as page_file:
                html = page_file.read()
                # Strip page body to improve performance
                html = re.split(self.body_pattern, html, maxsplit=1)[0]
                soup = BeautifulSoup(html, features="lxml")
                meta_element = soup.select_one("meta[name=\"description\"]")
                if meta_element:
                    count += 1
                    meta_descriptions[page_path] = meta_element.get("content")
                else:
                    meta_descriptions[page_path] = ""
        if count != len(self.pages):
            logger.warning(PLUGIN_TAG + f"Didn't find meta descriptions for {len(self.pages) - count} HTML pages")
        return meta_descriptions

    def write_csv(self):
        if self.meta_descriptions and self.meta_descriptions.keys():
            logger.info(PLUGIN_TAG + f"Writing {self.output_path}")
            with open(self.output_path, "w") as csv_file:
                csv_writer = csv.writer(csv_file)
                for page, meta_description in self.meta_descriptions.items():
                    csv_writer.writerow([os.path.relpath(page, self.site_dir), meta_description])
        else:
            logger.error(PLUGIN_TAG + "Can't find meta descriptions to write to CSV file")
