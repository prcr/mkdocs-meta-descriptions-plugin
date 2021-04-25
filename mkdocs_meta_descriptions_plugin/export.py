import os
import re
import logging
from urllib.parse import unquote
import csv

from bs4 import BeautifulSoup
from tqdm import tqdm

SITE_URL = r"https://docs\.codacy\.com"

logging.basicConfig(format="%(message)s", level=logging.INFO)


class Export():
    def __init__(self, site_dir, output_file="descriptions.csv"):
        self.site_dir = site_dir
        self.output_file = output_file

        self.sitemap = self.__parse_sitemap()
        self.pages = self.__read_descriptions()

    def __parse_sitemap(self):
        sitemap_path = os.path.join(self.site_dir, "sitemap.xml")
        if not os.path.isfile(sitemap_path):
            print("Can't open sitemap file")
            return None

        logging.info(f"Reading {sitemap_path}")
        with open(sitemap_path) as f:
            soup = BeautifulSoup(f.read(), features="lxml")
        logging.info(f"Sitemap references {len(soup.find_all('loc'))} pages")
        return soup

    def __read_descriptions(self):
        pages = {}
        logging.info("Reading meta descriptions from pages:")
        for loc in tqdm(self.sitemap.find_all("loc"), unit="pages"):
            # Transform URLs in local file names
            page_path = re.sub(SITE_URL + r"/(.*)",
                               r"\1index.html",
                               unquote(loc.text))
            with open(self.site_dir + "/" + page_path) as page_file:
                sitemap = BeautifulSoup(page_file, features="lxml")
                meta_element = sitemap.select_one("meta[name=\"description\"]")
                if meta_element:
                    pages[page_path] = meta_element.get("content")
                else:
                    pages[page_path] = "[No description found]"
        return pages

    def write_csv(self):
        output_path = os.path.join(self.site_dir, self.output_file)
        logging.info(f"Writing {output_path}")
        with open(output_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="\t")
            for key in self.pages.keys():
                csv_writer.writerow([key, self.pages[key]])
