import filecmp
import glob
import os.path
import tempfile
import subprocess

import pytest
from bs4 import BeautifulSoup
from click.testing import CliRunner
from mkdocs.__main__ import build_command
from mkdocs.structure.files import File, Files

mkdocs_yml_list = glob.glob("tests/*.yml")
markdown_files_list = [
    file[len("tests/docs/") :]
    for file in glob.glob("tests/docs/**/*.md", recursive=True)
]


def get_meta_description(files, markdown_file_path):
    html_file_path = files.get_file_from_path(markdown_file_path).abs_dest_path
    with open(html_file_path) as file:
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        result = soup.select_one('meta[name="description"]')
        return result["content"] if result else None


@pytest.fixture(
    scope="module",
    params=[True, False],
    ids=["use-directory-urls", "no-directory-urls"],
)
def use_directory_urls(request):
    flag = "--use-directory-urls" if request.param else "--no-directory-urls"
    return flag, request.param


@pytest.fixture(scope="module", params=mkdocs_yml_list)
def build(request, use_directory_urls):
    mkdocs_yml = request.param
    with tempfile.TemporaryDirectory() as tempdir:
        result = CliRunner().invoke(
            build_command,
            ["--config-file", mkdocs_yml, "--site-dir", tempdir, use_directory_urls[0]],
        )
        files = Files(
            [
                File(
                    file,
                    os.path.join(os.getcwd(), "tests/docs/"),
                    tempdir,
                    use_directory_urls[1],
                )
                for file in markdown_files_list
            ]
        )
        yield result, files, mkdocs_yml, use_directory_urls[1]


class TestPlugin:
    def test_build(self, build):
        result, _, _, _ = build
        assert result.exit_code == 0

    def test_build_output(self, build):
        _, files, _, _ = build
        for f in files:
            assert os.path.isfile(f.abs_dest_path)

    def test_index_md(self, build):
        _, files, _, _ = build
        expected = "For full documentation visit mkdocs.org."
        subprocess.Popen("ls")
        assert get_meta_description(files, "index.md") == expected
