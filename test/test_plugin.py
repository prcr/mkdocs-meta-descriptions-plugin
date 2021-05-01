import os
import pytest
import tempfile
from pathlib import Path

from mkdocs.__main__ import build_command

from bs4 import BeautifulSoup
from click.testing import CliRunner


def meta_description(html):
    soup = BeautifulSoup(html, features="lxml")
    result = soup.find("meta", {"name": "description"})
    return result["content"] if result else None


@pytest.fixture(params=["mkdocs.yml", "mkdocs-export-csv.yml"])
def build(request):
    config_file = Path("test") / request.param
    with tempfile.TemporaryDirectory() as tempdir:
        result = CliRunner().invoke(build_command,
                                    ["--config-file", config_file, "--site-dir", tempdir])
        output = {}
        for dirpath, _, files in os.walk(tempdir):
            for file in filter(lambda x: x.endswith((".html", ".csv")), files):
                file_path = Path(dirpath) / file
                output[file] = file_path.read_text() if file_path.exists() else None
        return result, output


@pytest.fixture
def output(build):
    return build[1]


class TestPluginBuild:
    def test_build(self, build):
        assert build[0].exit_code == 0, "MkDocs build failed"

    def test_html_output(self, output):
        for input_file in output:
            assert output[input_file] is not None

    def test_index(self, output):
        assert meta_description(output["index.html"]) == \
               "For full documentation visit mkdocs.org."

    def test_first_paragraph(self, output):
        assert meta_description(output["first_paragraph.html"]) == \
               "First paragraph."

    def test_first_paragraph_no_heading(self, output):
        assert meta_description(output["first_paragraph_no_heading.html"]) == \
               "First paragraph."

    def test_no_paragraph(self, output):
        assert meta_description(output["no_paragraph.html"]) == \
               "Value of site_description on mkdocs.yml"

    def test_first_paragraph_no_intro(self, output):
        assert meta_description(output["first_paragraph_no_intro.html"]) == \
               "Value of site_description on mkdocs.yml"

    def test_front_matter_description(self, output):
        assert meta_description(output["front_matter_description.html"]) == \
               "Value of meta description on front_matter_description.md"

    def test_escape_html_entities(self, output):
        assert meta_description(output["escape_html_entities.html"]) == \
               "First paragraph with HTML entities: \"quotes\", 'single quotes', "\
               "<greater and less than>, &ampersand&."
