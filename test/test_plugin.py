import os
import pytest
import tempfile
from pathlib import Path

from mkdocs.__main__ import build_command

from bs4 import BeautifulSoup
from click.testing import CliRunner


def meta_description(html):
    soup = BeautifulSoup(html, features="lxml")
    meta_description = soup.find("meta", {"name": "description"})
    return meta_description["content"] if meta_description else None


class TestPluginBuild:
    @pytest.fixture
    def test_build(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = CliRunner().invoke(build_command,
                                        ["--config-file", "mkdocs.yml", "--site-dir", tmpdir])

            assert result.exit_code == 0, "MkDocs build failed"

            output = {}
            for root, directories, files in os.walk("docs"):
                for name in files:
                    if name.endswith(".md"):
                        output_file = Path(tmpdir + "/" + name.replace(".md", ".html"))
                        assert output_file.exists(), f"{name} missing in output"
                        output[name] = output_file.read_text()

        return output

    def test_default(self, test_build):
        assert meta_description(test_build["index.md"]) == "Value of site_description on mkdocs.yml"
