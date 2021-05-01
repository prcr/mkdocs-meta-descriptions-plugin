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


class TestPluginBuild:
    @pytest.fixture
    def test_build(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = CliRunner().invoke(build_command,
                                        ["--config-file", "test/mkdocs.yml", "--site-dir", tmpdir])

            assert result.exit_code == 0, "MkDocs build failed"

            output = {}
            for _, _, files in os.walk("test/docs"):
                for name in files:
                    if name.endswith(".md"):
                        output_file = Path(tmpdir) / name.replace(".md", ".html")
                        assert output_file.exists(), f"{name} missing in output"
                        output[name] = output_file.read_text()

        return output

    def test_index(self, test_build):
        assert meta_description(test_build["index.md"]) == \
               "For full documentation visit mkdocs.org."

    def test_first_paragraph(self, test_build):
        assert meta_description(test_build["first_paragraph.md"]) == \
               "First paragraph."

    def test_first_paragraph_no_heading(self, test_build):
        assert meta_description(test_build["first_paragraph_no_heading.md"]) == \
               "First paragraph."

    def test_no_paragraph(self, test_build):
        assert meta_description(test_build["no_paragraph.md"]) == \
               "Value of site_description on mkdocs.yml"

    def test_first_paragraph_no_intro(self, test_build):
        assert meta_description(test_build["first_paragraph_no_intro.md"]) == \
               "Value of site_description on mkdocs.yml"

    def test_front_matter_description(self, test_build):
        assert meta_description(test_build["front_matter_description.md"]) == \
               "Value of meta description on front_matter_description.md"

    def test_escape_html_entities(self, test_build):
        assert meta_description(test_build["escape_html_entities.md"]) == \
               "First paragraph with HTML entities: \"quotes\", 'single quotes', "\
               "<greater and less than>, &ampersand&."
